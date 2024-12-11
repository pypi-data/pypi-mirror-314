"""Implements the grounding step of the KIE pipeline."""
import logging
from typing import List

import pandas as pd
from pyspark.sql.dataframe import DataFrame

from databricks.kie.data_utils import get_split_from_labeled, get_split_from_unlabeled
from databricks.kie.kie_state import KIEState
from databricks.kie.task_spec import KIETaskSpec
from databricks.model_serving.types.pt_endpoint import GenerationOutput, PayGoEndpoint
from databricks.model_serving.utils import MODEL_CONTEXT_LENGTH, ModelSpecs
from databricks.model_training.api.utils import get_spark

logger = logging.getLogger(__name__)


def calculate_fewshot_samples(tokens_processed: int, num_requests: int, current_samples: int) -> int:
    """
    Limit the number of fewshot examples based on the per-sample token average
    
    Context length is 131072 tokens, so we should leave plenty of room for the actual generation
    We'll leave 2 examples worth of space for the model to generate
    """
    tokens_per_example = tokens_processed / num_requests
    return max(min(current_samples, int(MODEL_CONTEXT_LENGTH / tokens_per_example) - 2), 0)


def create_grounding_df(
    base_df: pd.DataFrame,
    responses: List[GenerationOutput],
) -> DataFrame:
    spark = get_spark()
    response_strings, _ = zip(*responses)
    return spark.createDataFrame(pd.concat([base_df, pd.DataFrame(response_strings, columns=["response"])], axis=1))


def ground(task_spec: KIETaskSpec, state: KIEState, grounding_model: ModelSpecs) -> None:
    """
    Ground the task spec by running the grounding step.
    """
    if not state.requires_grounding:
        return

    if not grounding_model.endpoint:
        raise ValueError("Grounding model endpoint is not available")

    print('🌱 Selecting a few examples and extracting from them. This may take a moment...')
    if state.labeled_split_df:
        grounding_df = get_split_from_labeled(state.labeled_split_df, "grounding",
                                              task_spec.labeled_dataset_text_column,
                                              task_spec.labeled_dataset_output_json_column)
        logger.info(f"Got grounding df from labeled data. Using {grounding_df.count()} examples.")
    else:
        grounding_df = get_split_from_unlabeled(state.unlabeled_split_df, "grounding")
        logger.info(f"Got grounding df from unlabeled data. Using {grounding_df.count()} examples.")

    # Run inference using a strong model
    with PayGoEndpoint(grounding_model.endpoint) as endpoint:
        print("Extracting information from examples...")
        as_pd = grounding_df.toPandas()
        requests: List[str] = as_pd["request"].tolist()
        responses = endpoint.generate_batch(requests,
                                            system_prompt=state.ground_truth_prompt,
                                            response_format=state.response_format,
                                            show_progress=False)
        state.grounding_df = create_grounding_df(as_pd, responses)
        state.requires_grounding = False

        # Since we regenerated the grounding set, we'll need to update our downstream datasets
        state.requires_val = True
        state.requires_train_gen = True

        # Potentially limit fewshot examples based on size
        state.num_fewshot_samples = calculate_fewshot_samples(endpoint.tokens_processed, len(requests),
                                                              state.num_fewshot_samples)
