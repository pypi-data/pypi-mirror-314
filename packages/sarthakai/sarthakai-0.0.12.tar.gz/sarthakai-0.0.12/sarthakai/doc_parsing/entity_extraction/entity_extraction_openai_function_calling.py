import json
from openai import OpenAI
from typing import Dict

openai_client = OpenAI()


def entity_extraction_openai_function_calling(
    text_document: str, response_model: Dict
) -> Dict:
    function_definitions = [
        {
            "type": "function",
            "function": {
                "name": "extract_info",
                "description": "Get the information from the body of the input text",
                "parameters": {"type": "object", "properties": response_model},
            },
        }
    ]
    messages = [{"role": "user", "content": text_document}]
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=function_definitions
    )
    try:
        arguments = response.choices[0].message.tool_calls[0].function.arguments
        return json.loads(arguments)
    except Exception as e:
        print(e, response)
        return {}
