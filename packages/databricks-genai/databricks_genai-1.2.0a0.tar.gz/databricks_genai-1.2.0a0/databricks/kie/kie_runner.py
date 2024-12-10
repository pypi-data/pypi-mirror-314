"""Base runner for the KIE notebook"""
import sys
from typing import Dict, List, NamedTuple, Optional, Type, cast

import mlflow
from mlflow.entities import Run as MlflowRun
from pydantic import BaseModel
from pyspark.sql.dataframe import DataFrame

from databricks.kie.inference_utils import format_ai_query
from databricks.kie.kie_schema import ModelFactory
from databricks.kie.kie_state import KIEState
from databricks.kie.prompt_builder import PromptBuilder
from databricks.kie.steps.grounding import ground
from databricks.kie.steps.initialize import TaskInitializer, get_mlflow_experiment_link
from databricks.kie.steps.optimize import (SweepEvaluator, TrainingDataGenerator, ValidationDataGenerator,
                                           eval_baseline_models, launch_sweep)
from databricks.kie.steps.query_output import (get_prompts_from_run, prepare_output_table, ready_pt_endpoint_from_model,
                                               ready_pt_endpoint_from_run)
from databricks.kie.task_spec import KIETaskSpec
from databricks.model_serving.types.pt_endpoint import ProvisionedThroughputEndpoint
from databricks.model_serving.utils import get_model_specs
from databricks.model_training.api.utils import get_display


class KIEOutput(NamedTuple):
    endpoint: ProvisionedThroughputEndpoint
    ai_query: str


class KIERunner:
    """Runner class to be used in the KIE notebook"""
    task_spec: KIETaskSpec
    state: KIEState

    num_grounding_samples: int = 10
    num_val_samples: int = 25
    num_fewshot_samples: int = 3

    grounding_model_name = "balanced"
    optimized_model_names = ["cost-optimized"]

    def __init__(self, task_spec: KIETaskSpec):
        self.task_spec = task_spec
        initializer = TaskInitializer(task_spec)
        self.state = initializer.initialize(num_grounding_samples=self.num_grounding_samples,
                                            num_val_samples=self.num_val_samples,
                                            num_fewshot_samples=self.num_fewshot_samples)

        model_specs = get_model_specs()
        self.grounding_model = model_specs[self.grounding_model_name]
        assert self.grounding_model.endpoint is not None, "Grounding model must have an endpoint defined"
        assert self.grounding_model.uc_schema is not None, "Grounding model must have a UC schema path defined"
        self.optimized_models = [model_specs[name] for name in self.optimized_model_names]

    @property
    def response_format(self) -> Type[BaseModel]:
        return self.state.response_format

    @response_format.setter
    def response_format(self, response_format: Type[BaseModel]):
        self.recompile(response_format)

    @property
    def base_model_cost(self) -> float:
        return self.grounding_model.cost_per_hour

    @property
    def base_model_uc_schema(self) -> str:
        return self.grounding_model.uc_schema

    @property
    def ai_query(self) -> str:
        if not self.state.ai_query:
            raise ValueError("Please run `ready_ai_query_output` first")
        return self.state.ai_query

    def recompile(self, response_format: Type[BaseModel]):
        self.state.response_format = response_format

        # Cache the response format
        ModelFactory.to_file(self.state.response_format, self.state.schema_path)

        # Rebuild prompts
        self.state.prompt_builder = PromptBuilder(self.state.response_format)
        self.state.ground_truth_prompt = self.state.prompt_builder.build_prompt()
        self.state.zeroshot_prompt = self.state.prompt_builder.build_prompt(include_markdown=True)

        # Request that grounding be re-run
        self.state.requires_grounding = True

    def ground(self) -> DataFrame:
        ground(self.task_spec, self.state, self.grounding_model)

        # Update grounding cache
        assert self.state.grounding_df is not None  # We just grounded
        self.state.grounding_df.write.mode("overwrite").saveAsTable(self.state.grounding_table_path)

        return cast(DataFrame, self.state.grounding_df)

    def optimize(self, _gen_with_pt: bool = True) -> Dict[str, DataFrame]:
        # Generate validation data
        path = get_mlflow_experiment_link(self.state.experiment.experiment_id)
        print("Kicking off model optimizations. This step may take a while. " +
              f"You can track the progress at your MLflow experiment:\n{path}")

        val_generator = ValidationDataGenerator(self.task_spec,
                                                self.state,
                                                self.grounding_model,
                                                use_provisioned_throughput=_gen_with_pt)
        val_generator.generate()

        assert self.state.val_df is not None
        self.state.val_df.write.mode("overwrite").saveAsTable(self.state.val_table_path)

        # Feedback to user
        print("We'll test a few models using the validation dataset:\n")
        display = get_display()
        display(self.state.val_df.select("request", "expected_response").limit(10))  # TODO: This needs to flush somehow
        sys.stdout.flush()  # Maybe this will help?

        # Eval baseline models
        eval_baseline_models(self.task_spec, self.state, self.optimized_models)

        # Generate training data
        train_generator = TrainingDataGenerator(self.task_spec,
                                                self.state,
                                                self.grounding_model,
                                                use_provisioned_throughput=_gen_with_pt)
        train_generator.generate()

        # Launch the sweep
        launch_sweep(self.task_spec, self.state, self.optimized_models)

        # Follow sweep runs and eval models
        sweep_evaluator = SweepEvaluator(self.task_spec, self.state)
        sweep_evaluator.evaluate_sweep()

        assert self.state.model_dfs is not None
        return cast(Dict[str, DataFrame], self.state.model_dfs)

    def follow_optimizations(self) -> Dict[str, DataFrame]:
        sweep_evaluator = SweepEvaluator(self.task_spec, self.state)
        sweep_evaluator.evaluate_sweep()

        assert self.state.model_dfs is not None
        return cast(Dict[str, DataFrame], self.state.model_dfs)

    def ready_ai_query_output(self, use_baseline: bool = False, run_id: Optional[str] = None) -> KIEOutput:
        """Ready a PT endpoint and AI query command for the chosen model
        
        The PT endpoint will be created with "scale-to-zero" enabled, so it will automatically
        scale down when not in use.
        
        Args:
            use_baseline: Whether to use the baseline model
            run_id: The MLflow run ID of the model to use
        
        Returns:
            KIEOutput: A named tuple containing the `endpoint` and `ai_query` command
        
        Raises:
            ValueError: If neither `use_baseline` nor `run_id` is provided or if the run
                does not have all required artifacts
        """

        # Prepare the output table
        prepare_output_table(self.task_spec, self.state)

        # Stand-up an endpoint for the chosen model
        if use_baseline:
            endpoint = ready_pt_endpoint_from_model(self.base_model_uc_schema)
            system_prompt = trailing_prompt = self.state.zeroshot_prompt
        elif run_id:
            run = mlflow.get_run(run_id)
            endpoint = ready_pt_endpoint_from_run(run)
            system_prompt, trailing_prompt = get_prompts_from_run(run)
        else:
            raise ValueError("Please provide a run_id or set use_baseline=True")

        # Format the AI query command
        ai_query = format_ai_query(self.task_spec.output_table,
                                   endpoint,
                                   system_prompt=system_prompt,
                                   trailing_prompt=trailing_prompt)

        return KIEOutput(endpoint, ai_query)

    def choose_best_run(self) -> MlflowRun:
        # Get the best run from the experiment
        runs = mlflow.search_runs(experiment_ids=[self.state.experiment.experiment_id],
                                  filter_string="tags.registered_to LIKE '%'",
                                  order_by=["metrics.overall_score DESC"],
                                  max_results=1,
                                  output_format="list")
        runs = cast(List[MlflowRun], runs)
        if not runs:
            raise RuntimeError("Found no runs in the experiment that have been scored")
        return runs[0]
