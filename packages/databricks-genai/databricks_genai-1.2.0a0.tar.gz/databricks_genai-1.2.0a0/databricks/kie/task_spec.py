"""Defines the task spec for KIE"""
import os
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, model_validator

from databricks.kie.data_utils import IGNORED_CACHE_ROOT, get_valid_files
from databricks.model_training.api.exceptions import ValidationError
from databricks.model_training.api.utils import (check_if_table_exists, check_table_has_columns, get_me,
                                                 get_schema_from_table, get_spark, normalize_table_name)
from databricks.model_training.api.validation import (validate_delta_table, validate_uc_path_write_permissions,
                                                      validate_uc_permissions)


class KIETaskSpec(BaseModel):
    """Task spec for KIE experiments"""
    unlabeled_dataset: str
    json_examples: List[Dict[str, Any]]
    experiment_name: str
    labeled_dataset: Optional[str]
    labeled_dataset_text_column: str
    labeled_dataset_output_json_column: str
    output_path: str
    output_table: str

    @staticmethod
    def _get_default_output_path(unlabeled_dataset: str, experiment_name: str) -> str:
        # Default to a cache folder in the dataset
        root_name = os.path.basename(experiment_name).replace("-", "_")
        return os.path.join(unlabeled_dataset, f"{IGNORED_CACHE_ROOT}{root_name}")

    @staticmethod
    def _get_default_output_table(output_path: str, unlabeled_dataset: str) -> str:
        # Default to a table in the same schema as the input files
        output_schema = ".".join(output_path.split("/")[2:4])
        dataset_name = os.path.basename(unlabeled_dataset)
        return f"{output_schema}.{dataset_name}"

    @staticmethod
    def _get_default_experiment_name(unlabeled_dataset: str) -> str:
        # Choose a default experiment name
        # Extract dataset name from full path and normalize it
        unlabeled_dataset = os.path.basename(unlabeled_dataset.rstrip("/").replace("_", "-").lower())
        # Include user path
        username = get_me()
        return f"/Users/{username}/kie-{unlabeled_dataset}"

    @classmethod
    def create(
        cls,
        unlabeled_dataset: str,
        json_examples: List[Dict[str, Any]],
        experiment_name: Optional[str],
        labeled_dataset: Optional[str],
        labeled_dataset_text_column: str,
        labeled_dataset_output_json_column: str,
        output_path: Optional[str],
        output_table: Optional[str],
    ) -> 'KIETaskSpec':
        # Normalize path
        unlabeled_dataset = unlabeled_dataset.rstrip("/")

        if experiment_name is None:
            # Choose a default experiment name based on the dataset name
            experiment_name = cls._get_default_experiment_name(unlabeled_dataset)

        if output_path is None:
            output_path = cls._get_default_output_path(unlabeled_dataset, experiment_name=experiment_name)

        if output_table is None:
            output_table = cls._get_default_output_table(output_path, unlabeled_dataset)

        return cls(
            unlabeled_dataset=unlabeled_dataset,
            json_examples=json_examples,
            experiment_name=experiment_name,
            labeled_dataset=labeled_dataset,
            labeled_dataset_text_column=labeled_dataset_text_column,
            labeled_dataset_output_json_column=labeled_dataset_output_json_column,
            output_path=output_path,
            output_table=normalize_table_name(output_table),
        )

    @model_validator(mode='after')
    def validate_spec(self: 'KIETaskSpec') -> 'KIETaskSpec':
        try:
            return validate_task_spec(self)
        except ValidationError as e:
            # Re-raise validation errors for pydantic
            raise ValueError(str(e)) from e


def validate_can_read_from_unlabeled_dataset(unlabeled_dataset: str):
    try:
        os.listdir(unlabeled_dataset)
    except OSError as e:
        raise ValueError(f"Could not read from unlabeled dataset at {unlabeled_dataset}. " +
                         "Please make sure the path is correct and you have read permissions.") from e


def validate_schema_starting_point(task_spec: KIETaskSpec):
    if not task_spec.json_examples and not task_spec.labeled_dataset:
        raise ValueError("Please provide example JSON outputs so we can know what to extract")


def validate_output_write_permissions(output_path: str):
    try:
        os.makedirs(output_path, exist_ok=True)
    except OSError as e:
        raise ValueError(f"Could not create output folder at {output_path}. " +
                         "Please make sure you have write permissions to the parent directory, " +
                         "or specify an `output_path` where you do") from e

    validate_uc_path_write_permissions(output_path)


def validate_valid_output_path(output_path: str, unlabeled_dataset: str):
    if output_path.rstrip("/") == unlabeled_dataset.rstrip("/"):
        raise ValueError(
            "Output path cannot be the same as the unlabeled dataset. Please provide a different output path")

    if "." in output_path:
        raise ValueError("Output path cannot contain a '.' character. Please provide a different output path")


def validate_labeled_dataset_is_valid(labeled_dataset: str, labeled_dataset_text_column: str,
                                      labeled_dataset_output_json_column: str):
    spark = get_spark()
    labeled_df = spark.read.table(labeled_dataset)
    schema = dict(labeled_df.dtypes)

    # Validate the provided input column
    if labeled_dataset_text_column not in schema:
        raise ValueError(f"The provided labeled_dataset_text_column {labeled_dataset_text_column} " +
                         "is not in the table. Please check your configuration.")

    # Validate the provided output column, if specified
    if labeled_dataset_output_json_column not in schema:
        raise ValueError(f"The provided labeled_dataset_output_json_column {labeled_dataset_output_json_column} " +
                         "is not in the table. Please check your configuration.")


def validate_row_count(
    unlabeled_dataset: str,
    required_count: int = 10,
    recommended_count: int = 1000,
) -> None:
    all_files = get_valid_files(unlabeled_dataset)
    row_count = len(all_files)
    if row_count < required_count:
        raise ValueError(f'Insufficient data. We require at least {required_count} unlabeled examples ' +
                         f'(recommend at least {recommended_count}). Found only {row_count} examples.')
    if row_count < recommended_count:
        print(f'Warning: Found {row_count} unlabeled examples, ' +
              f'we recommend at least {recommended_count} for best results.')


def validate_task_spec(task_spec: KIETaskSpec) -> KIETaskSpec:

    # Validate that we can read from the unlabeled_dataset
    validate_can_read_from_unlabeled_dataset(task_spec.unlabeled_dataset)

    # Validate that we have enough unlabeled data to do anything
    validate_row_count(task_spec.unlabeled_dataset)

    # Validate that we have some schema starting point
    validate_schema_starting_point(task_spec)

    # Validate that the output path is valid
    validate_valid_output_path(task_spec.output_path, task_spec.unlabeled_dataset)

    # Validate permission to write to output paths
    validate_output_write_permissions(task_spec.output_path)
    print(f"✔ Validated write permissions to output_path: {task_spec.output_path}")

    # Validate we can write to the output schema
    output_schema = get_schema_from_table(task_spec.output_table)
    validate_uc_permissions(output_schema, 'schema', ['ALL_PRIVILEGES', 'USE_SCHEMA'], input_name='output_schema')

    # Ensure the output table doesn't already exist
    if check_if_table_exists(task_spec.output_table):
        # If output_table already exists, the user may be repeating KIE
        # Verify that it has a "request" column
        if not check_table_has_columns(task_spec.output_table, ("request",)):
            raise ValueError(f"Output table {task_spec.output_table} already exists, " +
                             "but does not seem to be from a KIE experiment. Please choose a different path.")

    print(f"✔ Validated write permissions to output_table: {task_spec.output_table}")

    # Validate the labeled dataset and ensure all columns specified exist
    if task_spec.labeled_dataset:
        # Validate that you can access the labeled_dataset
        validate_delta_table(task_spec.labeled_dataset, "labeled_dataset")

        # Validate the labeled dataset is valid
        validate_labeled_dataset_is_valid(task_spec.labeled_dataset, task_spec.labeled_dataset_text_column,
                                          task_spec.labeled_dataset_output_json_column)
        print(f"✔ Validated permissions and contents of labeled_dataset: {task_spec.labeled_dataset}")

    print("✔ Validation checks passed!")
    return task_spec
