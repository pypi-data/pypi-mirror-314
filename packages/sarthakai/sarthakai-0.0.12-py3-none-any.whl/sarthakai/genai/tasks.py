import json
from typing import List
from sarthakai.genai.prompts import (
    SummarisationSystemPrompt,
    QueryRoutingSystemPrompt,
    TableDescriptionGenerationSystemPrompt,
    TableReformattingSystemPrompt,
    IssueCheckingSystemPrompt,
)
from sarthakai.genai.llm import llm_call
from sarthakai.common import fuzzy_match_term_against_list_of_terms


def summarise_text(
    text_to_summarise: str, n_sentences: int, llm_name: str = "gpt-4o-mini"
):
    summarisation_system_prompt = SummarisationSystemPrompt(
        text_to_summarise=text_to_summarise, n_sentences=n_sentences
    )
    summarisation_messages = summarisation_system_prompt.messages
    summarised_text, cost = llm_call(messages=summarisation_messages, model=llm_name)
    return summarised_text


def route_query(query: str, routes: List[str], llm_name: str = "gpt-4o-mini"):
    query_routing_system_prompt = QueryRoutingSystemPrompt(query=query, routes=routes)
    query_routing_messages = query_routing_system_prompt.messages
    llm_predicted_route, cost = llm_call(
        messages=query_routing_messages, model=llm_name
    )

    fuzzy_matched_route = fuzzy_match_term_against_list_of_terms(
        term=llm_predicted_route, ground_truths=routes
    )
    return fuzzy_matched_route


def describe_table(
    table_to_describe: str, n_sentences: int = 2, llm_name: str = "gpt-4o-mini"
):
    table_description_generation_system_prompt = TableDescriptionGenerationSystemPrompt(
        table_to_describe=table_to_describe, n_sentences=n_sentences
    )
    table_description_generation_messages = (
        table_description_generation_system_prompt.messages
    )
    table_description_text, cost = llm_call(
        messages=table_description_generation_messages, model=llm_name
    )
    return table_description_text


def reformat_table(table_to_reformat: str, llm_name: str = "gpt-4o-mini"):
    table_reformatting_system_prompt = TableReformattingSystemPrompt(
        table_to_reformat=table_to_reformat
    )
    table_reformatting_messages = table_reformatting_system_prompt.messages
    reformatted_table, cost = llm_call(
        messages=table_reformatting_messages, model=llm_name
    )
    return reformatted_table


def check_if_answer_contains_issue(
    question: str,
    current_answer: str,
    issue: str,
    old_answer: str = "",
    additional_instructions: List[str] = None,
    llm_name: str = "gpt-4o",
    retries: int = 3,
):
    if not issue.strip():
        return False
    issue_checking_system_prompt = IssueCheckingSystemPrompt(
        question=question,
        current_answer=current_answer,
        issue=issue,
        old_answer=old_answer,
        additional_instructions=additional_instructions,
    )
    issue_checking_messages = issue_checking_system_prompt.messages
    try:
        llm_response, _ = llm_call(messages=issue_checking_messages, model=llm_name)
        llm_response = llm_response.replace("```json", "").replace("```", "")
        evaluation_result = json.loads(llm_response)
        return evaluation_result
    except Exception as e:
        print("ERROR", e)
        print(llm_response)
        if retries > 0:
            return check_if_answer_contains_issue(
                question=question,
                current_answer=current_answer,
                issue=issue,
                old_answer=old_answer,
                additional_instructions=additional_instructions,
                llm_name=llm_name,
                retries=retries - 1,
            )
        else:
            return {}
