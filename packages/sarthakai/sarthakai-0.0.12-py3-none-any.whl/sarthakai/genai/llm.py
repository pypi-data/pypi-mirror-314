import os
import requests
import json
import tiktoken
from litellm import completion, acompletion
from openai import OpenAI
from typing import List, Dict

million = 1000000
SONNET_MODEL_NAME = "claude-3-5-sonnet-20240620"
DEFAULT_LLM = "gpt-4o-mini"
pricing_usd = {
    "gpt-3.5-turbo": {"input": 0.50 / million, "output": 1.50 / million},
    "gpt-4o": {"input": 5 / million, "output": 15 / million},
    "gpt-4o-mini": {"input": 0.15 / million, "output": 0.60 / million},
}

openai_client = OpenAI()


def llm_call(messages, model=DEFAULT_LLM):
    response = completion(model=model, messages=messages)
    cost = (
        pricing_usd[model]["input"] * response.usage.prompt_tokens
        + pricing_usd[model]["output"] * response.usage.completion_tokens
    )
    return response.choices[0].message.content, cost


async def async_llm_call(messages, model=DEFAULT_LLM):
    response = await acompletion(model=model, messages=messages)
    cost = (
        pricing_usd[model]["input"] * response.usage.prompt_tokens
        + pricing_usd[model]["output"] * response.usage.completion_tokens
    )
    return {"response": response.choices[0].message.content, "cost": cost}


def num_tokens_from_messages(messages, model=DEFAULT_LLM):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model or "omni" in model:
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def chunk_local_file_reducto(filename: str, chunk_size: int = None):
    url = "https://api.reducto.ai/chunk_file?llm_table_summary=false&figure_summarization=false&no_chunk=false"
    if chunk_size:
        url += "&chunk_size=" + str(chunk_size)

    files = {"document_file": (filename, open(filename, "rb"), "application/pdf")}
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + os.environ["REDUCTO_API_KEY"],
    }
    try:
        response = requests.post(url, files=files, headers=headers)
        return json.loads(response.text)
    except:
        print(response.text)


def chunk_file_by_url_reducto(document_url: str, chunk_size: int = None):
    url = f"https://api.reducto.ai/chunk_url?llm_table_summary=false&document_url={document_url}"

    if chunk_size:
        url += "&chunk_size=" + str(chunk_size)

    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + os.environ["REDUCTO_API_KEY"],
    }
    try:
        response = requests.post(url, headers=headers)
        return json.loads(response.text)
    except:
        print(response.text)


def get_embedding_batch(input_array):
    chunk_size = 200
    embeddings_list = []
    for i in range(0, len(input_array), chunk_size):
        array_subset = input_array[i : i + chunk_size]
        response = openai_client.embeddings.create(
            input=array_subset, model="text-embedding-3-small"
        )
        embeddings_list += [data.embedding for data in response.data]

    return embeddings_list
