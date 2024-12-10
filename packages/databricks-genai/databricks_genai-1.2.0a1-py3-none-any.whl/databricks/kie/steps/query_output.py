"""Prepare the user to run ai_query on their data"""

import os
from typing import Tuple, cast

import mlflow
from mlflow import MlflowException
from mlflow.entities import Run as MlflowRun

from databricks.kie.constants import MLFLOW_REGISTERED_MODEL_TAG, MLFLOW_SYSTEM_PROMPT_FILE, MLFLOW_TRAILING_PROMPT_FILE
from databricks.kie.data_utils import get_all_unlabeled
from databricks.kie.kie_state import KIEState
from databricks.kie.task_spec import KIETaskSpec
from databricks.model_serving.types.pt_endpoint import ProvisionedThroughputEndpoint
from databricks.model_training.api.utils import check_if_table_exists, check_table_has_columns


def prepare_output_table(task_spec: KIETaskSpec, state: KIEState):
    """Prepare the output table for ai_query"""

    if check_if_table_exists(task_spec.output_table) and check_table_has_columns(task_spec.output_table, ("request",)):
        print(f"Output table {task_spec.output_table} already exists with the correct schema.")
        return

    # Read the data into a DataFrame and write it to a Delta table
    print("Preparing output table for ai_query")
    print(f"Reading documents into {task_spec.output_table}. This may take a moment...")
    df = get_all_unlabeled(state.unlabeled_split_df)
    df.write.mode("overwrite").saveAsTable(task_spec.output_table)


def get_model_from_run(run: MlflowRun) -> str:
    """Get the model UC schema from an mlflow run based on the registered_to tag
    """
    # Get the model from the run
    if MLFLOW_REGISTERED_MODEL_TAG not in run.data.tags:
        raise ValueError("This run is not registered to a model through the KIE notebook."
                         f"Set a tag on the run with `{MLFLOW_REGISTERED_MODEL_TAG}` to the UC schema of the model.")

    uc_schema = run.data.tags[MLFLOW_REGISTERED_MODEL_TAG]
    return uc_schema


def get_prompts_from_run(run: MlflowRun) -> Tuple[str, str]:
    """Get the system and trailing prompts from an mlflow run
    """
    if not run.info.artifact_uri:
        raise ValueError("This run does not have an artifact URI")

    try:
        root_uri = cast(str, run.info.artifact_uri)
        system_prompt = mlflow.artifacts.load_text(os.path.join(root_uri, MLFLOW_SYSTEM_PROMPT_FILE))
        trailing_prompt = mlflow.artifacts.load_text(os.path.join(root_uri, MLFLOW_TRAILING_PROMPT_FILE))
    except MlflowException as e:
        raise ValueError(
            "This run does not have the system and trailing prompts saved as artifacts."
            f"Make sure the prompts are saved as `{MLFLOW_SYSTEM_PROMPT_FILE}` and `{MLFLOW_TRAILING_PROMPT_FILE}`"
        ) from e

    return system_prompt, trailing_prompt


def ready_pt_endpoint_from_run(run: MlflowRun) -> ProvisionedThroughputEndpoint:
    """Create a PT endpoint from an mlflow run
    """
    # Get the tag on the mlflow run
    model_uc_schema = get_model_from_run(run)

    # Create the PT endpoint
    endpoint = ProvisionedThroughputEndpoint(model_uc_schema, block_until_ready=False)

    # Create the PT endpoint
    return endpoint


def ready_pt_endpoint_from_model(model_uc_schema: str) -> ProvisionedThroughputEndpoint:
    """Create a PT endpoint from a model UC schema
    """
    return ProvisionedThroughputEndpoint(model_uc_schema, block_until_ready=False)
