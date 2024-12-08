import os
import instructor
from openai import OpenAI
from anthropic import Anthropic


def extract_extraction_instructor(
    text_document: str,
    response_model,
    llm_provider: str = "openai",
    llm_name: str = "gpt-4o",
    retries=5,
):
    """Uses Instructor to extract small details in a structured format, from a huge document."""
    try:
        if llm_provider == "openai":
            client = instructor.from_openai(
                OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            )
        elif llm_provider == "anthropic":
            client = instructor.from_anthropic(
                Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
            )
        # Extract structured data from text document
        instructor_result = client.chat.completions.create(
            model=llm_name,
            response_model=response_model,
            messages=[{"role": "user", "content": text_document}],
        )
        return instructor_result
    except Exception as e:
        if retries > 0:
            return extract_extraction_instructor(
                text_document=text_document,
                response_model=response_model,
                llm_provider=llm_provider,
                llm_name=llm_name,
                retries=retries - 1,
            )
        else:
            return None
