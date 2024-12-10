"""Module implementaion of entrypoint API for Text2Text."""

import random
from collections import defaultdict
from typing import Dict, List, Optional

import mlflow
import pandas as pd
import requests as request_lib
from mlflow import create_experiment, get_experiment_by_name, get_trace, start_run, start_span
from mlflow.metrics.genai import make_genai_metric_from_prompt
from mlflow.models import infer_signature
from pyspark.sql.dataframe import DataFrame as PySparkDataFrame

from databricks.kie.t2t_custom_model import CustomModel, ModelWrapper
from databricks.kie.t2t_utils import (INSTRUCTION_AND_INPUT_PROMPT_TEMPLATE, LLM_JUDGE_EVAL_PROMPT_TEMPLATE,
                                      EvaluationCriteria, generate_evaluation_criteria)
from databricks.model_training.api.utils import get_host_and_token_from_env


def to_row_based_format(column_based_data: Dict[str, List[str]]) -> List[Dict[str, str]]:
    """
    Converts column-based data to row-based format.

    Args:
        column_based_data (dict): A dictionary where keys are column names and values are lists of column values.

    Returns:
        list: A list of dictionaries where each dictionary represents a row of data.
    """
    row_based_data = []
    num_rows = len(next(iter(column_based_data.values())))
    for i in range(num_rows):
        row = {key: value[i] for key, value in column_based_data.items()}
        row_based_data.append(row)
    return row_based_data


def to_column_based_format(row_based_data: List[Dict[str, str]]) -> Dict[str, List[str]]:
    """
    Converts row-based data to column-based format.

    Args:
        row_based_data (list): A list of dictionaries where each dictionary represents a row of data.

    Returns:
        dict: A dictionary where keys are column names and values are lists of column values.
    """
    if not row_based_data:
        return {}

    column_based_data = {key: [] for key in row_based_data[0].keys()}
    for row in row_based_data:
        for key, value in row.items():
            column_based_data[key].append(value)
    return column_based_data


class Text2TextRunner:
    """
    A class to manage the Text2Text model lifecycle, including training, evaluation, and deployment.

    Main API:
    - compile(): Optimizes prompt / model given provided hyperparameters.
    - update_state(): Updates the state of the runner with new instruction, evaluation criteria, or example data.
    - evaluate_models(): Evaluates all models in the runner.
    - visualize_models(): Visualizes model predictions for a subset of test data.
    - deploy_model(): Deploys a model to a production endpoint.
    """
    NUM_FEW_SHOTS = [0, 3, 5]
    MIN_EVAL_DATA = 5
    MAX_EXAMPLES_FOR_VISUALIZATION = 5
    MODEL_SELECTION = [
        "databricks-meta-llama-3-70b-instruct", "llama-3-1-405b", "gpt-4o-2024-08-06", "gpt-4o-mini-2024-07-18",
        "gpt-35-turbo-1106"
    ]

    def __init__(self,
                 experiment_name: str,
                 instruction: str,
                 evaluation_criteria: Optional[EvaluationCriteria] = None,
                 query_result: Optional[PySparkDataFrame] = None,
                 request_column_name: Optional[str] = None,
                 response_column_name: Optional[str] = None,
                 example_json: Optional[List[Dict[str, str]]] = None):
        """
        Initializes the Text2TextRunner with the provided parameters.

        One of `query_result` or `example_json` must be provided. 
        If `query_result` is provided, `request_column_name` and `response_column_name` must also be provided.

        Args:
            experiment_name (str): The name of the MLflow experiment.
            instruction (str): The instruction for the Text2Text model.
            evaluation_criteria (Optional[EvaluationCriteria]): Criteria for evaluating the models.
            query_result (Optional[PySparkDataFrame]): Query result as a PySpark DataFrame.
            request_column_name (Optional[str]): Column name for requests in the query result.
            response_column_name (Optional[str]): Column name for responses in the query result.
            example_json (Optional[List[Dict[str, str]]]): Example data in JSON format.
        """
        self.instruction = instruction
        self.model_map = defaultdict(list)
        self.test_data: List[Dict[str, str]] = []
        self.train_data: List[Dict[str, str]] = []

        example_data = None
        if not example_json and not query_result:
            raise ValueError("Must provide either query_result or example_json")

        if example_json:
            example_data = to_column_based_format(example_json)
            if set(example_data.keys()) != {"request", "response"}:
                raise ValueError("example_json must be list of dict with `request` and `response` keys only.")
        else:
            if not query_result or not request_column_name or not response_column_name:
                raise ValueError(("Must provide query_result, request_column_name,"
                                  "and response_column_name when using example_json=None"))
            example_data = {
                "request": query_result.select("*").toPandas()[request_column_name].tolist(),
                "response": query_result.select("*").toPandas()[response_column_name].tolist(),
            }

        self.example_data: Dict[str, List[str]] = example_data
        self._partition_data()

        self.eval_criteria: Optional[EvaluationCriteria] = evaluation_criteria
        if not self.eval_criteria:
            self.eval_criteria = generate_evaluation_criteria(self.instruction, self.train_data)

        self.experiment_id = self._get_exp_id(experiment_name)
        self._create_models()
        self.display_params()

    # TODO(jun.choi): Implement this method
    # Integrate with auto rag  / ft / DSPy for prompt optimization.
    def compile(self):
        raise NotImplementedError

    def display_params(self):
        """Displays the current parameter of the runner."""
        print('========= PARAMS ============')
        print(f"INSTRUCTION: {self.instruction}\n")
        print(f"eval criteria : {self.eval_criteria}\n")
        print(f"examples : {self.example_data}\n")
        print("=============================")

    def update_state(self,
                     eval_criteria: Optional[EvaluationCriteria] = None,
                     instruction: Optional[str] = None,
                     example_data: Optional[List[Dict[str, str]]] = None) -> None:
        """Updates the state of the runner with new instruction, evaluation criteria, or example data."""
        if instruction:
            self.instruction = instruction

        if eval_criteria:
            self.eval_criteria = eval_criteria

        if example_data:
            self.example_data = to_column_based_format(example_data)

        self.display_params()

    def evaluate_models(self):
        """Evaluates all models in the runner using the provided evaluation criteria."""
        result = {}
        for model_wrappers in self.model_map.values():
            for model_wrapper in model_wrappers:
                model_eval = self._evaluate_model(model_wrapper)
                result[model_wrapper.custom_model.model_descriptor] = model_eval
        return pd.DataFrame.from_dict(result)

    def visualize_models(self):
        """Runs a subset of test data through each model and returns the results."""
        result = {}
        for model_wrappers in self.model_map.values():
            for model_wrapper in model_wrappers:
                result[model_wrapper.custom_model.model_descriptor] = self._visualize_model(model_wrapper)
        return pd.DataFrame.from_dict(result)

    def deploy_model(self, model_descriptor, schema_name, endpoint_name):
        model_wrapper = None
        all_model_desc = []
        for model_wrappers in self.model_map.values():
            for model_wrapper_candidate in model_wrappers:
                all_model_desc.append(model_wrapper_candidate.custom_model.model_descriptor)

                if model_wrapper_candidate.custom_model.model_descriptor == model_descriptor:
                    model_wrapper = model_wrapper_candidate
                    break

        if not model_wrapper:
            raise ValueError(f"invalid model descriptor.. input: `{model_descriptor}` candidates: {all_model_desc}")

        self._register_model(model_wrapper, schema_name)

        model_url = model_wrapper.get_model_path()
        production_model = mlflow.pyfunc.load_model(model_url)
        api_url, api_token = get_host_and_token_from_env()
        data = {
            "name": endpoint_name,
            "config": {
                "served_entities": [{
                    "entity_name": model_wrapper.registered_model_name,
                    "entity_version": '1',
                    "workload_size": "Small",
                    "scale_to_zero_enabled": True,
                    "environment_vars": {
                        "API_URL": api_url,
                        "API_TOKEN": api_token,
                    }
                }]
            }
        }

        headers = {"Context-Type": "text/json", "Authorization": f"Bearer {api_token}"}

        response = request_lib.post(url=f"{api_url}/api/2.0/serving-endpoints", json=data, headers=headers, timeout=60)
        print("Deployed endpoint.. Response status:", response.status_code)
        print("Deployed endpoint.. Response text:", response.text, "\n")
        return production_model

    def _get_exp_id(self, experiment_name: str):
        experiment = get_experiment_by_name(experiment_name)
        if not experiment:
            return create_experiment(name=experiment_name)
        return experiment.experiment_id

    def _partition_data(self):
        """Randomly sample half of example_data to test data and other half to train data."""
        example_data_size = len(self.example_data['request'])
        if example_data_size < self.MIN_EVAL_DATA:
            self.test_data = to_row_based_format(self.example_data)
            return

        indices = list(range(example_data_size))
        random.shuffle(indices)
        split_index = example_data_size // 2

        train_indices = indices[:split_index]
        test_indices = indices[split_index:]

        self.train_data = [{
            "request": self.example_data['request'][i],
            "response": self.example_data['response'][i]
        } for i in train_indices]
        self.test_data = [{
            "request": self.example_data['request'][i],
            "response": self.example_data['response'][i]
        } for i in test_indices]

    def _create_models(self):
        print(f"Registering models..{self.MODEL_SELECTION}")
        for model_id in self.MODEL_SELECTION:
            for n in self.NUM_FEW_SHOTS:
                if n > len(self.train_data):
                    break

                model = self._create_text2text_model(model_id, num_few_shot=n)
                self.model_map[model_id].append(model)

    def _register_model(self, model_wrapper: ModelWrapper, schema_path: str):
        custom_model = model_wrapper.custom_model
        run_id = model_wrapper.run_id
        model_name = custom_model.model_descriptor.replace('.', '-')
        registered_model_name = f'{schema_path}.t2t_{model_name}'
        model_wrapper.registered_model_name = registered_model_name
        with start_run(experiment_id=self.experiment_id, run_id=run_id):
            mlflow.pyfunc.log_model("model",
                                    python_model=custom_model,
                                    pip_requirements=["pandas", "dspy-ai", "mlflow"],
                                    signature=custom_model.signature,
                                    registered_model_name=registered_model_name)

    def _create_text2text_model(self, model_id: str, num_few_shot: int = 0):
        with start_run(
                experiment_id=self.experiment_id,
                run_name=f't2x_model_registry_{model_id}_few_shot_{num_few_shot}',
        ) as run:
            few_shot_examples = []
            if num_few_shot:
                few_shot_examples = random.sample(self.train_data, num_few_shot)

            signature = infer_signature(model_input=self.example_data['request'],
                                        model_output=self.example_data['response'])

            custom_model = CustomModel(
                self.instruction,
                signature,
                model_id,
                few_shot_examples,
            )
            run_id = run.info.run_id
            return ModelWrapper(custom_model, run_id, registered_model_name=None)

    def _visualize_model(self, model_wrapper: ModelWrapper):
        custom_model = model_wrapper.custom_model
        model_results = []
        for datum in self.test_data[0:self.MAX_EXAMPLES_FOR_VISUALIZATION]:
            req = datum['request']
            output_dict = {}
            output_dict["input"] = req
            output_dict["label"] = datum['response']
            output_dict["model_output"] = custom_model.predict(None, req)
            model_results.append(output_dict)
        return model_results

    def _evaluate_model(self, model_wrapper: ModelWrapper):
        if not self.eval_criteria:
            raise ValueError("Evaluation criteria is not provided")

        custom_model = model_wrapper.custom_model
        requests = [
            INSTRUCTION_AND_INPUT_PROMPT_TEMPLATE.format(instruction=self.instruction, inp=datum['request'])
            for datum in self.test_data
        ]
        ground_truth = [datum['response'] for datum in self.test_data]

        eval_result = {}
        model_desc = model_wrapper.custom_model.model_descriptor
        for eval_criteria_info in self.eval_criteria.criteria:
            eval_criteria = eval_criteria_info.eval_criterion
            yes_is_better = eval_criteria_info.yes_is_better

            with start_run(nested=True,
                           experiment_id=self.experiment_id,
                           parent_run_id=model_wrapper.run_id,
                           run_name=f'eval_{model_desc}_{eval_criteria}'):

                model_responses = []
                traces = []
                for req in requests:
                    with start_span(f"{model_desc}") as span:
                        model_response = custom_model.predict(None, req)

                    traces.append(get_trace(span.request_id).to_json())
                    model_responses.append(model_response)

                judge_prompt = LLM_JUDGE_EVAL_PROMPT_TEMPLATE.format(
                    eval_criteria=eval_criteria
                ) + "\n The instruction & request is : '{request}' \n  Model Response is: '{response}'"

                custom_eval_metric = make_genai_metric_from_prompt(
                    name=eval_criteria,
                    judge_prompt=judge_prompt,
                    metric_metadata={"assessment_type": "ANSWER"},
                    model="endpoints:/databricks-meta-llama-3-1-405b-instruct",
                    greater_is_better=yes_is_better)

                eval_df = pd.DataFrame({
                    "request": requests,
                    "expected_response": ground_truth,
                    "response": model_responses,
                    "trace": traces
                })

                result = mlflow.evaluate(
                    data=eval_df,
                    model_type="databricks-agent",  # Enable Mosaic AI Agent Evaluation
                    extra_metrics=[custom_eval_metric],
                )

                eval_result[eval_criteria] = result
        return eval_result
