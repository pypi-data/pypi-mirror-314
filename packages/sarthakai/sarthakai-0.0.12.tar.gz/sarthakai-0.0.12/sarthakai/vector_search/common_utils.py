from openai import OpenAI
from typing import List

from sarthakai.models import Chunk
from sarthakai.genai.llm import llm_call
from sarthakai.genai.prompts import QuestionAnsweringSystemPrompt

openai_client = OpenAI()


def get_embedding_batch(input_array: List[str], model: str = "text-embedding-3-large"):
    batch_size = 1000
    embeddings_list = []
    input_array = [" " if item == "" else item for item in input_array]
    for i in range(0, len(input_array), batch_size):
        try:
            array_subset = input_array[i : i + batch_size]

            response = openai_client.embeddings.create(input=array_subset, model=model)
            embeddings_list += [i.embedding for i in response.data]

        except Exception as e:
            print(e, array_subset)
            break
    return embeddings_list


def answer_question(query: str, context_documents: List[str]):
    question_answering_system_prompt = QuestionAnsweringSystemPrompt(
        context_documents=context_documents
    )
    question_answering_system_prompt = question_answering_system_prompt.compile()
    messages = [
        {"role": "system", "content": question_answering_system_prompt},
        {"role": "user", "content": query},
    ]
    llm_response = llm_call(messages)
    return llm_response


def filter_document_search_results_llm(user_prompt, search_results: List[Chunk]):
    chunk_size = 100
    relevant_docs = ""
    for i in range(0, len(search_results), chunk_size):
        chunk = search_results[i : i + chunk_size]
        system_prompt = """Out of the following documents, return only those which are absolutely necessary to answer the user's question.
        Return your answer as a bulletted list in new lines. If none of the documents is relevant, return 'NONE'."""
        # print(chunk)
        for doc in chunk:
            system_prompt += "\n- " + doc["document"]
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        llm_response = llm_call(messages)
        if "NONE" in llm_response:
            break
        relevant_docs += llm_response
    return relevant_docs, search_results
