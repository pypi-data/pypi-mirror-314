"""Module that encapsulates instruction analysis for Text2Text."""

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from databricks.kie.inference_utils import generate_base_model_using_chat_completion_messages

INSTRUCTION_INFO_GENERATION_SYSTEM_PROMPT = """
You are an expert in instruction analysis and generation. That is, given a list of JSON objects containing `request` and `response` keys,
you should `infer` the OPTIMAL instruction to generate the response given the request. Instructions should be as detailed as possible.

The instruction info to generate has the following fields:
- optimized_instruction: string instruction that can be used to create the response given the request.
- output_format: Format of the output string. This should detail formatting constraints of the output. 
        Example output formats includes guidlines such as:
        e.g)    - 'Output should be a comma separated list'
                - 'Response should be as concise as possible'
                - 'Response should be json with keys a, b, c'
                - 'Response should not contains phrases like...'
                - 'Response should have the tone of ...'

- instruction_type: Enum that describes the type of instruction. Can be one of : {instruction_type_list}

The list of JSON objects containing `request` and `response` keys is provided after the header `example_data` below:
example_data: {data}
"""

INSTRUCTION_INFO_GENERATION_SYSTEM_PROMPT_WITH_INSTRUCTIONS = """
You are an expert in instruction analysis / generation. That is, given 
  - a list of JSON objects containing `request` and `response` keys
  - the original instruction provided by the user

you should `infer` the OPTIMAL instruction to generate the response given the request. Instructions should be as detailed as possible.
The instruction info to generate has following fields.

- optimized_instruction: string instruction that can be used to create the response given the request.
- output_format: Format of the output string. This should detail formatting constraints of the output. 
        Example output formats includes guidlines such as:
        e.g)    - 'Output should be a comma separated list'
                - 'Response should be as concise as possible'
                - 'Response should be json with keys a, b, c'
                - 'Response should not contains phrases like...'
                - 'Response should have the tone of ...'

- instruction_type: Enum that describes the type of instruction. Can be one of : {instruction_type_list}

The list of JSON objects containing `request` and `response` keys is provided after the header `example_data`.
The original instruction provided by the user is provided after the header `original_instruction`.

example_data: {data}
original_instruction: {instruction}
"""


class InstructionType(str, Enum):
    classification = "classification"
    grounded_generation = "grounded_generation"
    subspan_extraction = "subspan_extraction"
    summarization = "summarization"
    others = "others"


# TODO(jun.choi): Add `optimized_instruction` in InstructionSchema via DSPY
class InstructionInfo(BaseModel):
    optimized_instruction: str = Field(
        description="""Instruction optimized for the model. Includes detailed guidelines including
        1. Instruction / task description.
        2. Nature of the input to be provided.
        3. Expected response format.
        """)
    instruction_type: InstructionType = Field(description=("Task type of of the instruction. Can be one of :"
                                                           f"{ ', '.join(str(v.name) for v in InstructionType) }"))
    output_format: str = Field(
        description=("The format of the output response. For example "
                     "'Output should be a comma separated list' / 'Response should be as concise as possible' "))


def generate_instruction_info(
    example_data: List[Dict[str, str]],
    instruction: Optional[str] = None,
):
    instruction_type_list = f"{ ', '.join(str(v.name) for v in InstructionType) }"
    system_msg = (INSTRUCTION_INFO_GENERATION_SYSTEM_PROMPT_WITH_INSTRUCTIONS.format(
        data=example_data, instruction=instruction, instruction_type_list=instruction_type_list) if instruction else
                  INSTRUCTION_INFO_GENERATION_SYSTEM_PROMPT.format(data=example_data,
                                                                   instruction_type_list=instruction_type_list))
    messages = [{"role": "system", "content": system_msg}]

    return generate_base_model_using_chat_completion_messages(messages, InstructionInfo)
