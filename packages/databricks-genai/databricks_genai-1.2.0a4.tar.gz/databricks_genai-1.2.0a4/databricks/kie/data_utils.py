"""Simple utils for working with KIE datasets"""
import json
import os
import warnings
from functools import wraps
from typing import Any, Dict, Iterable, List, Optional, Tuple, Type

import pandas as pd
from pydantic import BaseModel, ValidationError
from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import monotonically_increasing_id, rand
from pyspark.sql.types import StringType, StructField, StructType
from pyspark.sql.window import Window

from databricks.kie.kie_evaluator import parse_json_markdown
from databricks.model_serving.types.pt_endpoint import BaseEndpoint
from databricks.model_training.api.utils import get_spark

VALID_EXTENSIONS = {
    '.c', '.cpp', '.cs', '.css', '.go', '.html', '.java', '.js', '.json', '.md', '.php', '.py', '.rb', '.sh', '.tex',
    '.ts', '.txt', ''
}

MIN_LABELED_TRAIN_SAMPLES = 100
MIN_DOCS_TO_TRAIN = 50

IGNORED_CACHE_ROOT = 'kie_cache_'


def cache_on_serverless(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        spark = get_spark()
        return spark.createDataFrame(result.toPandas())

    return wrapper


def get_split_from_labeled(labeled_split_df: DataFrame, split: str, request: str, expected_response: str) -> DataFrame:
    # yapf: disable
    return (labeled_split_df
            .where(F.col('split') == split)
            .withColumn('request', F.col(request))
            .withColumn('expected_response', F.col(expected_response))
    )  # yapf: enable


@cache_on_serverless
def get_split_from_unlabeled(unlabeled_split_df: DataFrame, split: str) -> DataFrame:
    # yapf: disable
    df = (unlabeled_split_df
            .where(F.col('split') == split)
            .withColumn('request', F.udf(read_document, StringType())(F.col('doc_uri')))
    )
    return df # yapf: enable

def get_all_unlabeled(unlabeled_split_df: DataFrame) -> DataFrame:
    """Get all unlabeled data from the split df """
    # yapf: disable
    df = (unlabeled_split_df
            .withColumn('request', F.udf(read_document, StringType())(F.col('doc_uri')))) # yapf: enable
    return df


def get_valid_files(directory: str) -> List[str]:
    """ Recursively get all files in the directory that match valid extensions
    """
    all_files = []
    for root, _, files in os.walk(directory):
        if os.path.basename(root).startswith(IGNORED_CACHE_ROOT):
            # This is a cache folder - skip it
            continue
        for f in files:
            if os.path.splitext(f)[1].lower() in VALID_EXTENSIONS:
                all_files.append(os.path.join(root, f))

    return all_files


def split_labeled_data(
    df: DataFrame,
    num_grounding_samples: int = 5,
    num_val_samples: int = 25,
    seed: int = 42,
) -> DataFrame:

    # Count the total sample size
    total_samples = df.count()

    # Allocate first to grounding, then val and training
    labeled_remaining = total_samples

    num_grounding_samples = min(num_grounding_samples, labeled_remaining)
    labeled_remaining -= num_grounding_samples

    # Create random data splits
    # Order by rand so we can sample from it
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', message='.*WindowExpression.*')
        df = df.withColumn('rand', F.rand(seed=seed)).withColumn('row_id', F.row_number().over(Window.orderBy('rand')))

    df = df.withColumn('split', F.lit('train'))
    df = df.withColumn('split',
                       F.when(F.col('row_id') <= num_grounding_samples, F.lit('grounding')).otherwise(F.col('split')))
    df = df.withColumn('split',
                       F.when((F.col('row_id') > num_grounding_samples) & \
                              (F.col('row_id') <= num_grounding_samples + num_val_samples),
                              F.lit('val')).otherwise(F.col('split')))

    return df


def split_unlabeled_data(
    dataset: str,
    num_val_samples: int = 25,
    num_grounding_samples: int = 5,
    seed: int = 42,
) -> DataFrame:

    # Find all available files in the UC volume
    all_files = get_valid_files(dataset)

    if not all_files:
        raise ValueError(f"No files found in {dataset} matching accepted file types: {','.join(VALID_EXTENSIONS)}")

    # Create a dataframe with the file paths
    spark = get_spark()
    schema = StructType([StructField('doc_uri', StringType(), True)])

    # Create DataFrame with schema
    df = spark.createDataFrame([(uri,) for uri in all_files], schema=schema).orderBy('doc_uri')

    # Calculate how many unlabeled samples we have
    total_files = len(all_files)

    # Adjust sample counts to respect max percentages
    max_grounding = max(int(total_files * 0.10), 1)  # 10% max for grounding
    max_val = max(int(total_files * 0.20), 1)  # 20% max for validation

    # Calculate needed samples respecting maximums
    grounding_needed = min(num_grounding_samples, max_grounding)
    val_needed = min(num_val_samples, max_val)

    # Order by rand so we can sample from it
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', message='.*WindowExpression.*')
        df = df.withColumn('rand', F.rand(seed=seed)).withColumn('row_id', F.row_number().over(Window.orderBy('rand')))

    # Order by random value and create splits
    running_count = 0

    df = df.withColumn('split', F.lit('unused'))
    if grounding_needed > 0:
        df = df.withColumn('split',
                           F.when(F.col('row_id') <= grounding_needed, F.lit('grounding')).otherwise(F.col('split')))
        running_count += grounding_needed

    if val_needed > 0:
        df = df.withColumn(
            'split',
            F.when((F.col('row_id') > running_count) & (F.col('row_id') <= running_count + val_needed),
                   F.lit('val')).otherwise(F.col('split')))
        running_count += val_needed

    return df.select('doc_uri', 'split').orderBy('doc_uri')


def read_document(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def get_fewshot_examples(
    df: DataFrame,
    num_examples: int,
    response_format: Type[BaseModel],
    response_column: str = 'expected_response',
) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Extract valid few-shot examples from the provided DataFrame.

    Args:
        df: DataFrame containing request/response pairs
        num_examples: Number of examples to extract
        response_format: Expected format for validation
        response_column: Column containing the expected response

    Returns:
        List of (request, response) tuples
    """
    examples = []
    for row in df.limit(num_examples).collect():
        try:
            response = json.loads(row[response_column])
            response_format(**response)  # Validate response
            examples.append((row['request'], response))
            if len(examples) >= num_examples:
                break
        except (json.JSONDecodeError, ValidationError):
            continue
    return examples

def filter_valid_json(df: DataFrame, column_name: str, schema: Type[BaseModel]) -> DataFrame:
    spark = get_spark()

    # Convert to pandas
    pdf = df.toPandas()

    # Validate each row
    valid_mask = pdf[column_name].apply(lambda x: _is_valid_json(x, schema))

    # Filter and convert back to Spark
    filtered_pdf = pdf[valid_mask]
    return spark.createDataFrame(filtered_pdf, df.schema)

def _is_valid_json(maybe_json_str: str, schema: Type[BaseModel]) -> bool:
    try:
        schema(**json.loads(maybe_json_str))
        return True
    except:  # pylint: disable=bare-except
        return False


def _make_training_row(
    prompt: str,
    request: str,
    response: str,
) -> dict:
    user_message = prompt + '\n\nDocument:\n\n' + request.replace('"', '').replace('“', '').replace(
        '”', '') + '\n\n' + prompt
    messages = [{
        'role': 'user',
        'content': user_message
    }, {
        'role': 'assistant',
        'content': parse_json_markdown(response)
    }]
    messages_line = {'messages': messages}
    return messages_line


def process_for_sampling(df: DataFrame, seed: int = 42) -> DataFrame:
    spark = get_spark()
    df_shuffled = df.orderBy(rand(seed=seed))
    df_with_id = df_shuffled.withColumn('id', monotonically_increasing_id())
    df_with_id_static = spark.createDataFrame(df_with_id.toPandas())
    return df_with_id_static


def batched_iterator(df: DataFrame, batch_size: int = 1000) -> Iterable[pd.DataFrame]:
    current_max_index = 0
    while current_max_index < df.count():
        yield df.where((df.id >= current_max_index) & (df.id < current_max_index + batch_size)).withColumn(
            'request',
            F.udf(read_document, StringType())(F.col('doc_uri'))).toPandas()  # type: ignore
        current_max_index += batch_size


def write_batch_to_cache(prompt: str,
                         documents: List[str],
                         responses: List[str],
                         response_format: Type[BaseModel],
                         train_jsonl_cache_path: str):
    lines = []
    for request, response in zip(documents, responses):
        if not _is_valid_json(response, response_format):
            continue

        training_row = _make_training_row(
            prompt=prompt,
            request=request,
            response=response,
        )
        lines.append(json.dumps(training_row))

    with open(train_jsonl_cache_path, 'a', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n' if lines else '')



def create_training_data(
    unlabeled_split_df: DataFrame,
    prompt: str,
    response_format: Type[BaseModel],
    train_jsonl_cache_path: str,
    endpoint: BaseEndpoint,
    token_budget: int = 7_000_000,
    min_docs_to_train: int = MIN_DOCS_TO_TRAIN,
) -> Optional[Tuple[str, int]]:

    # Math to determine how many tokens to generate maximum
    # We are going to run a sweep across 3 learning rates, {2, 4} epochs
    # Target total pricing is $500
    # 8b is $4/M tokens or 6 DBU/M token
    # So $500 gives us 500/4 = 125M tokens to work with
    # We ideally want to 18 epochs (3 learning rates * 6 epochs per learning rate) total
    # This gives us 125M/18 ~= 7M tokens per epoch

    train_df = unlabeled_split_df.where((F.col('split') == 'train') | (F.col('split') == 'unused'))

    if train_df.count() < min_docs_to_train:
        return None

    ready_for_sampling = process_for_sampling(train_df)

    token_budget_remaining = token_budget
    for batch in batched_iterator(ready_for_sampling):
        documents = batch['request'].tolist()

        responses = endpoint.generate_batch(
            prompts=documents,
            system_prompt=prompt,
            total_max_tokens=token_budget_remaining,
            response_format=response_format,
            show_progress=False,
        )

        actual_responses = [r.response for r in responses]

        write_batch_to_cache(prompt, documents, actual_responses, response_format, train_jsonl_cache_path)
        token_budget_remaining -= sum(r.total_tokens for r in responses)
    return train_jsonl_cache_path, token_budget - token_budget_remaining


def validate_row_count(
    df: DataFrame,
    required_count: int = 10,
    recommended_count: int = 1000,
) -> None:
    row_count = df.count()
    if row_count < required_count:
        raise ValueError(f'Insufficient data. Found {row_count} rows, expected at least {required_count}.')
    if row_count < recommended_count:
        print(f'Warning: Found {row_count} rows, recommended at least {recommended_count} for best results.')
