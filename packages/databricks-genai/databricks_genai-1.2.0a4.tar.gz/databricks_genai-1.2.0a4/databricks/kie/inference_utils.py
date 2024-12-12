"""Inference utility functions to invoke LLM's using ChatCompletionsRequest."""
import json
from typing import Any, Dict, List, Optional

import requests as request_lib
from pydantic import BaseModel

from databricks.model_serving.types.pt_endpoint import BaseEndpoint
from databricks.model_training.api.utils import get_host_and_token_from_env, normalize_table_name

try:
    from openai.lib._parsing._completions import type_to_response_format_param
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# TODO(jun.choi): Make client ID configurable per usecase.
CLIENT_ID = 'finetuning'

# Constants
MARKDOWN_JSON_PATTERN = r'(?s).*?```(?:json)?\s*(.*?)\s*```\s*.*'
DOCUMENT_TEMPLATE = "\\n\\nDocument:\\n\\n"


def clean_request_text(text_col: str) -> str:
    """Create SQL to clean request text.
    
    Args:
        text_col: Column containing text to clean
    """
    return rf"""REPLACE(REPLACE(REPLACE({text_col}, '"', ''), '“', ''), '”', '')"""


def format_ai_query(
    source: str,
    endpoint: BaseEndpoint,
    system_prompt: str,
    max_tokens: int = 1024,
    temperature: float = 0.3,
    trailing_prompt: Optional[str] = None,
) -> str:
    """Format SQL query for AI extraction.
    
    Args:
        source: Source table name
        endpoint: Endpoint for AI queries
        system_prompt: System prompt for extraction

        
    Example:
        >>> query = format_ai_query(
        ...     source="my_table",
        ...     endpoint=my_endpoint,
        ...     system_prompt="Extract entities",
        ...     max_tokens=2048,
        ...     temperature=0.5,
        ... )
    
    Returns:
        Formatted SQL query string
    """

    # Handle table name quoting
    table_name = normalize_table_name(source)

    # Handle trailing prompt
    trailing_prompt = trailing_prompt or system_prompt

    # Build query components
    model_params = f"named_struct('max_tokens', {max_tokens}, 'temperature', {temperature})"
    clean_request = clean_request_text("request")

    full_prompt = f"""
        system_prompt || 
        '{DOCUMENT_TEMPLATE}' || 
        {clean_request} || 
        '\\n\\n' || 
        trailing_prompt
    """

    return f"""
    SELECT 
        *,
        CASE 
            WHEN extracted_response != '' THEN extracted_response 
            ELSE raw_response 
        END AS response
    FROM (
        SELECT 
            *,
            ai_query(
                '{endpoint.endpoint.name}',
                {full_prompt},
                failOnError => true,
                modelParameters => {model_params}
            ) AS raw_response,
            regexp_extract(raw_response, r'{MARKDOWN_JSON_PATTERN}', 1) AS extracted_response
        FROM {table_name}
        CROSS JOIN (
            SELECT 
                '{system_prompt}' AS system_prompt,
                '{trailing_prompt}' AS trailing_prompt
        )
    )
    """


def _create_request_db(chat_completions, model_id, timeout=None):
    api_url, api_token = get_host_and_token_from_env()
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    api_path = f'{api_url}/api/2.0/conversation/proxy/chat/completions'
    payload = {
        '@method': 'databricksChatCompletionRequest',
        'params': {
            **chat_completions
        },
        'model': model_id,
        'metadata': {
            'clientId': CLIENT_ID
        },
    }
    return request_lib.post(api_path, headers=headers, json=payload, timeout=timeout)


def _create_request_ext(chat_completions, model_id, timeout=None):
    api_url, api_token = get_host_and_token_from_env()
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    api_path = f'{api_url}/api/2.0/conversation/proxy/chat/completions'

    payload = {
        '@method': 'openAiServiceChatCompletionRequest',
        'params': {
            **chat_completions
        },
        'model': model_id,
        'apiVersion': '2024-09-01-preview',
        'metadata': {
            'clientId': CLIENT_ID
        },
    }
    return request_lib.post(api_path, headers=headers, json=payload, timeout=timeout)


_MODEL_FN_DICT = {
    'databricks-meta-llama-3-70b-instruct': _create_request_db,
    'llama-3-1-405b': _create_request_db,
    'gpt-4o-2024-08-06': _create_request_ext,
    'gpt-4o-mini-2024-07-18': _create_request_ext,
    'gpt-4-0613': _create_request_ext,
    'gpt-4-turbo-2024-04-09': _create_request_ext,
    'gpt-35-turbo-1106': _create_request_ext
}


def get_llm_proxy_chat_completion_response(model_id: str, req: Dict, timeout: Optional[float] = None) -> str:
    """Retrieves the chat completion response from a specified language model.
    k
        Args:
            model_id (str): The identifier of the language model to use.
            req (dict): The request payload to be sent to the language model.

        Returns:
            str: The content of the chat completion response.
    """
    if model_id not in _MODEL_FN_DICT:
        raise ValueError(f'Model id {model_id} is not supported. Please use one of {_MODEL_FN_DICT.keys()}')

    response = _MODEL_FN_DICT[model_id](req, model_id, timeout=timeout)

    if response.status_code != 200:
        raise RuntimeError(f'Request failed with status code {response.status_code}: {response.text}')

    out = json.loads(response.json()['completion'])['choices'][0]['message']['content']
    return out


def generate_base_model_using_chat_completion_messages(messages: List[Dict[str, str]], model_clz: Any) -> BaseModel:
    if not OPENAI_AVAILABLE:
        raise ImportError("openai library is not available. Please install it to use this")

    req: Dict = {
        'messages': messages,
        'response_format': type_to_response_format_param(model_clz),
    }

    res = get_llm_proxy_chat_completion_response('gpt-4o-2024-08-06', req)
    return model_clz(**json.loads(res))
