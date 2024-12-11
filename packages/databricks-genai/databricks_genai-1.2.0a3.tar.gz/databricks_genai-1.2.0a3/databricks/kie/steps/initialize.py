"""Iniitialize the KIE task and load cached values"""
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Type
from urllib.parse import urljoin

import mlflow
from databricks.sdk import WorkspaceClient  # pylint: disable = ungrouped-imports
from mlflow.entities import Experiment
from pydantic import BaseModel
from pyspark.sql import DataFrame

from databricks.kie.data_utils import split_labeled_data, split_unlabeled_data
from databricks.kie.kie_schema import ModelFactory
from databricks.kie.kie_state import KIEState
from databricks.kie.prompt_builder import PromptBuilder
from databricks.kie.task_spec import KIETaskSpec
from databricks.model_training.api.utils import get_browser_url, get_schema_from_table, get_spark


def get_table_if_exists(path: str) -> Optional[DataFrame]:
    # Load files from cache if they exist
    wc = WorkspaceClient()
    try:
        if wc.tables.exists(path).table_exists:
            spark = get_spark()
            return spark.read.table(path)
    except:  # pylint: disable=bare-except
        return None


def get_mlflow_experiment_link(experiment_id: str) -> str:
    """
    Get a link for the MLflow experiment using the given link text.
    This link will open the MLflow experiment page in a new tab.
    """
    host = get_browser_url()
    path = urljoin(host, f'/ml/experiments/{experiment_id}')
    return path


@dataclass
class CachePaths:
    """Holds all cache paths for a KIE task."""
    unlabeled_table: str
    labeled_table: str
    grounding_table: str
    val_table: str
    train_jsonl: str
    schema_json: str

    @classmethod
    def from_task_spec(cls, task_spec: KIETaskSpec, root_name: str) -> 'CachePaths':
        output_schema = get_schema_from_table(task_spec.output_table)
        cache_root = f"{output_schema}.{root_name}"

        return cls(unlabeled_table=f"{cache_root}_unlabeled",
                   labeled_table=f"{cache_root}_labeled",
                   grounding_table=f"{cache_root}_grounding",
                   val_table=f"{cache_root}_val",
                   train_jsonl=str(Path(task_spec.output_path) / f"{root_name}_train.jsonl"),
                   schema_json=str(Path(task_spec.output_path) / f"{root_name}_schema.json"))


class TaskInitializer:
    """Initializes a KIE task's state from a task spec"""

    def __init__(self, task_spec: KIETaskSpec):
        self.task_spec = task_spec
        self.spark = get_spark()

    def _setup_experiment(self) -> Experiment:
        """Setup and return MLflow experiment."""
        experiment = mlflow.get_experiment_by_name(self.task_spec.experiment_name)
        if experiment is None:
            experiment_id = mlflow.create_experiment(self.task_spec.experiment_name)
            experiment = mlflow.get_experiment(experiment_id)
            path = get_mlflow_experiment_link(experiment.experiment_id)
            print(f"🧪 Created a new MLflow experiment at: [link={path}]{path}[/link]")
        else:
            path = get_mlflow_experiment_link(experiment.experiment_id)
            print(f"🧪 Using MLflow experiment at: [link={path}]{path}[/link]")
        return experiment

    def _get_response_format(self, cache_paths: CachePaths) -> Type[BaseModel]:
        """Get or create response format."""
        if os.path.exists(cache_paths.schema_json):
            return ModelFactory.from_file(cache_paths.schema_json)

        if self.task_spec.labeled_dataset and not self.task_spec.json_examples:
            labeled_df = self.spark.read.table(self.task_spec.labeled_dataset)
            rows = labeled_df.limit(10).collect()
            self.task_spec.json_examples = [
                json.loads(r[self.task_spec.labeled_dataset_output_json_column]) for r in rows
            ]

        return ModelFactory.from_examples(self.task_spec.json_examples, "response_format")

    def _setup_data_splits(self, cache_paths: CachePaths, num_grounding_samples: int,
                           num_val_samples: int) -> Tuple[Optional[DataFrame], DataFrame]:
        """Setup labeled and unlabeled data splits."""

        labeled_split_df = get_table_if_exists(cache_paths.labeled_table)
        if self.task_spec.labeled_dataset and labeled_split_df is None:
            labeled_df = self.spark.read.table(self.task_spec.labeled_dataset)
            labeled_split_df = split_labeled_data(labeled_df,
                                                  num_grounding_samples=num_grounding_samples,
                                                  num_val_samples=num_val_samples)
            labeled_split_df.write.mode("overwrite").saveAsTable(cache_paths.labeled_table)
            num_val_samples = num_grounding_samples = 0
            print(f"Sourcing labeled data from {self.task_spec.labeled_dataset}")

        unlabeled_split_df = get_table_if_exists(cache_paths.unlabeled_table)
        if unlabeled_split_df is None:
            unlabeled_split_df = split_unlabeled_data(self.task_spec.unlabeled_dataset,
                                                      num_val_samples=num_val_samples,
                                                      num_grounding_samples=num_grounding_samples)
            unlabeled_split_df.write.mode("overwrite").saveAsTable(cache_paths.unlabeled_table)

        print(f"Found {unlabeled_split_df.count()} unlabeled documents to extract")
        return labeled_split_df, unlabeled_split_df

    def initialize(self, num_grounding_samples: int, num_val_samples: int, num_fewshot_samples: int) -> KIEState:
        """Initialize KIE task state."""
        experiment = self._setup_experiment()
        root_name = os.path.basename(experiment.name).replace("-", "_")
        cache_paths = CachePaths.from_task_spec(self.task_spec, root_name)

        response_format = self._get_response_format(cache_paths)
        prompt_builder = PromptBuilder(response_format)

        labeled_split_df, unlabeled_split_df = self._setup_data_splits(cache_paths, num_grounding_samples,
                                                                       num_val_samples)

        grounding_df = get_table_if_exists(cache_paths.grounding_table)
        val_df = get_table_if_exists(cache_paths.val_table)

        return KIEState(
            experiment=experiment,
            prompt_builder=prompt_builder,
            ground_truth_prompt=prompt_builder.build_prompt(),
            zeroshot_prompt=prompt_builder.build_prompt(include_markdown=True),
            fewshot_prompt=None,
            grounding_table_path=cache_paths.grounding_table,
            val_table_path=cache_paths.val_table,
            train_jsonl_path=cache_paths.train_jsonl,
            schema_path=cache_paths.schema_json,
            requires_grounding=grounding_df is None,
            requires_val=val_df is None,
            requires_train_gen=not os.path.exists(cache_paths.train_jsonl),
            unlabeled_split_df=unlabeled_split_df,
            labeled_split_df=labeled_split_df,
            grounding_df=grounding_df,
            val_df=val_df,
            response_format=response_format,
            num_grounding_samples=num_grounding_samples,
            num_val_samples=num_val_samples,
            num_fewshot_samples=num_fewshot_samples,
            model_dfs=None,
        )
