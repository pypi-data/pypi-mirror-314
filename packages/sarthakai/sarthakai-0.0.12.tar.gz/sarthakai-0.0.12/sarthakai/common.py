import string
import random
from rapidfuzz import fuzz, process
from typing import List


def generate_random_id(k: int = 48):
    random_id = "".join(
        random.choices(string.ascii_letters, k=k)
    )  # initializing size of string
    return random_id


def fuzzy_match_term_against_list_of_terms(
    term: str, ground_truths: List[str], threshold: str = 80
) -> str:
    if not ground_truths:
        raise Exception("List `ground_truths` cannot be empty.")
    terms_and_matching_scores = process.extract(
        term.lower(),
        ground_truths,
        scorer=fuzz.partial_ratio,
        limit=2,
    )
    return [term for term, score, _ in terms_and_matching_scores if score >= threshold][
        0
    ]


def clean_llm_json_response(llm_response):
    """Remove ```json and ``` from LLM responses."""
    cleaned_response = llm_response.replace("```json", "").replace("```", "")
    return cleaned_response
