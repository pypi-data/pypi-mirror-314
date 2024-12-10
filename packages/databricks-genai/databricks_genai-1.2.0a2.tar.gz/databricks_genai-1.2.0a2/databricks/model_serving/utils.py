"""Utils for working with model serving"""

from typing import NamedTuple, Optional

from mlflow import MlflowClient

MODEL_CONTEXT_LENGTH = 131072


class ModelSpecs(NamedTuple):
    name: str
    endpoint: Optional[str]
    cost_per_hour: float
    ft_model_name: str
    is_hosted: bool = True
    uc_schema: Optional[str] = None
    version: Optional[str] = None


def get_latest_model_version(model_name: str) -> str:
    """Get the latest version of a model using Mlflow

    Args:
        model_name (str): The name of the model

    Returns:
        str: The latest version of the model
    """
    client = MlflowClient()
    model_versions = client.search_model_versions(f"name='{model_name}'")

    if not model_versions:
        raise ValueError(f"No model versions found for model '{model_name}'")

    version_numbers = [int(model.version) for model in model_versions]
    most_recent_version = max(version_numbers)
    return str(most_recent_version)


def get_model_by_ft_name(ft_model_name: str) -> Optional[str]:
    model_specs = get_model_specs()
    for model_spec in model_specs.values():
        if model_spec.ft_model_name == ft_model_name:
            return model_spec.name


def get_model_specs():
    model_specs = {
        'balanced':
            ModelSpecs("balanced",
                       endpoint='databricks-meta-llama-3-1-70b-instruct',
                       cost_per_hour=29.70,
                       ft_model_name='meta-llama/Meta-Llama-3.1-70B-Instruct',
                       uc_schema='system.ai.meta_llama_v3_1_70b_instruct',
                       version=get_latest_model_version('system.ai.meta_llama_v3_1_70b_instruct')),
        'cost-optimized':
            ModelSpecs("cost-optimized",
                       endpoint=None,
                       cost_per_hour=7.42,
                       ft_model_name='meta-llama/Meta-Llama-3.1-8B-Instruct',
                       is_hosted=False,
                       uc_schema='system.ai.meta_llama_v3_1_8b_instruct',
                       version=get_latest_model_version('system.ai.meta_llama_v3_1_8b_instruct')),
    }
    return model_specs
