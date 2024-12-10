"""Holds the state of a KIE experiment"""
from typing import Dict, Optional, Type, Union

from mlflow.entities import Experiment
from pydantic import BaseModel, ConfigDict
from pyspark.sql.connect.dataframe import DataFrame as ConnectDataFrame
from pyspark.sql.dataframe import DataFrame as SparkDataFrame

from databricks.kie.prompt_builder import PromptBuilder

DataFrame = Union[SparkDataFrame, ConnectDataFrame]


class KIEState(BaseModel):
    """Holds the state of a KIE experiment"""
    experiment: Experiment  # The experiment to use for training
    ground_truth_prompt: str  # The prompt to use for ground truth generation

    prompt_builder: PromptBuilder
    zeroshot_prompt: str  # The prompt to use for zero-shot learning
    fewshot_prompt: Optional[str]  # The prompt to use for few-shot learning

    grounding_table_path: str  # Path to the grounding table
    val_table_path: str  # Path to the validation table
    train_jsonl_path: str  # Dataset path for training
    schema_path: str  # Path to the schema

    requires_grounding: bool  # Whether grounding is required
    requires_val: bool  # Whether validation is required
    requires_train_gen: bool  # Whether training data generation is required

    unlabeled_split_df: DataFrame  # Unlabeled data
    labeled_split_df: Optional[DataFrame]  # Labeled data
    grounding_df: Optional[DataFrame]  # Grounding data
    val_df: Optional[DataFrame]  # Validation data
    model_dfs: Optional[Dict[str, DataFrame]]  # Run-specific dataframes with eval data

    response_format: Type[BaseModel]  # The response format for the task

    num_grounding_samples: int  # Number of grounding samples
    num_val_samples: int  # Number of validation samples
    num_fewshot_samples: int  # Number of few-shot samples

    model_config = ConfigDict(
        protected_namespaces=(),
        arbitrary_types_allowed=True,
    )
