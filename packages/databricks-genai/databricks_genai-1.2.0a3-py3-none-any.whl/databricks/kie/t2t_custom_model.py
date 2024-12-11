"""Module to encapsulate LLM invocation logic as custom MLFLow PythonModel."""

from typing import Dict, List, Optional

import mlflow
from mlflow.models import ModelSignature
from mlflow.pyfunc import PythonModelContext

from databricks.kie.inference_utils import get_llm_proxy_chat_completion_response
from databricks.kie.t2t_utils import create_chat_completions_messages_from_instruction, create_chat_completions_request


class CustomModel(mlflow.pyfunc.PythonModel):
    """
    A custom MLflow Python model that processes inputs based on provided instructions.

    Args:
        instruction (str): The instruction guiding the model's behavior.
        example_data (dict): A dictionary containing 'request' and 'response' examples for model signature inference.
        model_id (str): The identifier of the underlying language model to use for generating predictions.
    """

    def __init__(self,
                 instruction: str,
                 signature: ModelSignature,
                 model_id: str,
                 few_shot_examples: Optional[List[Dict[str, str]]] = None):
        self.instruction = instruction
        self.model_id = model_id
        self.few_shot_examples = few_shot_examples or []
        suffix = f"fewshot_{len(self.few_shot_examples)}" if len(self.few_shot_examples) > 0 else "zero_shot"
        self.model_descriptor = f"{model_id}_{suffix}"
        self.signature = signature

    def predict(self, context: PythonModelContext, model_input: str, params: Optional[Dict] = None):
        del context, params
        messages = create_chat_completions_messages_from_instruction(self.instruction, model_input)
        req = create_chat_completions_request(messages)
        return get_llm_proxy_chat_completion_response(self.model_id, req)


class ModelWrapper():

    def __init__(self, custom_model: CustomModel, model_run_id: str, registered_model_name: Optional[str] = None):
        self.custom_model = custom_model
        self.run_id = model_run_id
        self.registered_model_name = registered_model_name

    def get_model_path(self):
        return f"runs:/{self.run_id}/model"
