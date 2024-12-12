"""Utility functions for abstract out request construction / response parsing of Text-to-Text tasks."""

import json
from typing import Dict, List, Optional

from openai.lib._parsing._completions import type_to_response_format_param
from pydantic import BaseModel, Field

from databricks.kie.inference_utils import get_llm_proxy_chat_completion_response

INSTRUCTION_AND_INPUT_PROMPT_TEMPLATE = """
Instruction : {instruction}

User input : {inp}
"""

LLM_JUDGE_EVAL_PROMPT_TEMPLATE = """
Your task is to evaluate and determine whether the provided `response` meets the below `evaluation criteria`. 
You are given input instruction, response, and evaluation criteria.
input instruction is provided following the header: `input`.
response is provided following the header `response`.
evaluation criteria is provided following the header `evaluation criteria`.

You should output a 5 if there `response` perfectly met/satisfied the evaluation critieria, and 1 if response did not meet the evaluation criteria.

evaluation criteria: '{eval_criteria}'
"""

EVAL_CRITERIA_GENERATOR_SYSTEM_PROMPT = (
    "You are an expert at user instruction analysis. "
    "Given an instruction for any task provided by the user, return a JSON list of criteria."
    "The criteria will be used to score an LLM on how well it followed the instructions given a specific input."
    "Provide detailed granular evaluation criteria on fomatting, style, and correctness."
    "Instruction to analyze is provided in in user message following 'Instruction' header."
    "Provide detailed granular evaluation criteria on fomatting, style, and correctness.")

EVAL_CRITERIA_GENERATOR_SYSTEM_PROMPT_WITH_EXAMPLES = (
    "You are an expert at user instruction analysis. "
    "Given an instruction for any task provided by the user and a JSON containing ground truth request"
    " and response pairs, return a JSON list of criteria."
    "The criteria will be used to score an LLM on how well it followed the instructions given a specific input."
    "Instruction to analyze is provided in in user message following 'Instruction' header, "
    "and examples are provided in user message following 'Ground Truth Examples' header."
    "Provide detailed granular evaluation criteria on fomatting, style, and correctness.")

SYSTEM_PROMPT_TEMPLATE = """
You are a helpful AI Agent. Please follow the following instructions with given input.
The instruction provided by the user is included following the "Instruction" header below.
The instruction describes the general task that the user would like to accomplish.

Instruction : '{instruction}'

The specific input for this request is included in the as part of user message.
"""

USER_PROMPT_TEMPLATE = """
user input : '{inp}'
"""

EVAL_PROMPT_TEMPLATE = """
Your task is to evaluate the response using the following criteria given input and response.

evaluation criteria: '{eval_criteria}'
"""

EVAL_PROMPT_SUFFIX = """
 This is the input: '{request}'
 This is the model output to evaluate: '{response}'
"""

CHAIN_OF_THOUGHT_SYSTEM_PROMPT = """
Given instruction and user input provided as the system message and user messages above, generate CoT class.

CoT class provide a detailed step-by-step reasoning that leads to answering the provided user instruction.
CoT class has 2 fields: `step_by_step_reasoning` and `concise_response`.

step_by_step_reasoning : please provide detailed step-by-step reasoning that leads to answering the provided user instruction.
concise_response: please provide the most correct and concise answer to the user instruction.

If few shot examples are provided in the user messages above, refer to assistant messages in few shot examples
to infer the `concise_response` fields. Note that previous assistant output to few shot examples does not
include the `step_by_step_reasoning`. If few shot examples exists as messages above, refer to them as
examples for generating the `concise_response` field.
"""


class EvaluationCriterion(BaseModel):

    eval_criterion: str = Field(
        description="Granular evaluation criteria to evaluate another model's output to the instruction.",)
    yes_is_better: bool = Field(description="Whether yes to the evaluation criteria is good or not.",)


class EvaluationCriteria(BaseModel):
    criteria: List[EvaluationCriterion]

    model_config = {"json_schema_extra": {"title": "evaluation_criteria", "additionalProperties": False}}


class CoT(BaseModel):
    step_by_step_reasoning: str = Field(
        description="Detailed step by step reasoning that leads to answering the provided user instruction.")
    concise_response: str = Field(description="The most correct and concise answer to the user instruction.")


def create_chat_completions_request(messages: List[Dict[str, str]], response_format: Optional[Dict] = None):
    """
    Creates a chat completions request json.

    Args:
        messages (list): A list of message dictionaries to be included in the request.
        response_format (str, optional): The desired format of the response. Defaults to None.

    Returns:
        dict: A dictionary representing the chat completions request.
    """
    chat_completion_req: Dict = {
        "messages": messages,
    }
    if response_format:
        chat_completion_req['response_format'] = response_format
    return chat_completion_req


def create_chat_completions_messages_from_instruction(instruction: str, inp: str):
    """
    Creates a list of chat completion messages based on the given instruction and input.

    Args:
        instruction (str): The instruction to be included in the system message.
        inp (str): The input to be included in the user message.

    Returns:
        list: A list of dictionaries representing the chat messages. Each dictionary contains
              a 'role' key (either 'system' or 'user') and a 'content' key with the respective message.
    """

    messages = [{
        "role": "system",
        "content": SYSTEM_PROMPT_TEMPLATE.format(instruction=instruction)
    }, {
        "role": "user",
        "content": USER_PROMPT_TEMPLATE.format(inp=inp)
    }]
    return messages


def generate_evaluation_criteria(instruction: str, examples: Optional[List[Dict]] = None) -> EvaluationCriteria:
    """Generates list of evaluation criteria based on the given instruction and examples.

    Args:
        instruction (str): The instruction to generate evaluation criteria for.
        examples (list, optional): A list of dictionaries containing ground truth request and response pairs.
            Defaults to None.

    Returns:
        list: A list of EvaluationCriterion objects.
    """
    messages = [{
        "role":
            "system",
        "content":
            EVAL_CRITERIA_GENERATOR_SYSTEM_PROMPT_WITH_EXAMPLES if examples else EVAL_CRITERIA_GENERATOR_SYSTEM_PROMPT
    }, {
        "role":
            "user",
        "content": (f"Instruction: {instruction}\n\n Ground Truth Examples: {json.dumps(examples)}"
                    if examples else f"Instruction: {instruction}")
    }]

    req = create_chat_completions_request(messages, type_to_response_format_param(EvaluationCriteria))
    res = get_llm_proxy_chat_completion_response("gpt-4o-2024-08-06", req)
    return EvaluationCriteria(**json.loads(res))


def generate_cot_response(model_id: str, messages: List[Dict]) -> str:
    """
    Generates a response that has gone through CoT reasoning.
    
    Note: CHAIN of thought reasoning is not returned -- it is used only for improving reasoning
    as model autoregressively generates the response tokens.
    The implementation is structured such that chain of thought reasoning is always generated first.

    Args:
        model_id (str): The model identifier to use for generating the response.
        messages (list): A list of message dictionaries to be included in the request.
            Corresponds to chat completion messges.
    
    Returns:
        str: The most correct and concise answer to the user instruction
    """
    messages.append({"role": "system", "content": CHAIN_OF_THOUGHT_SYSTEM_PROMPT})
    req = create_chat_completions_request(messages, type_to_response_format_param(CoT))
    res = get_llm_proxy_chat_completion_response(model_id, req)
    cot_response = CoT(**json.loads(res))
    return cot_response.concise_response
