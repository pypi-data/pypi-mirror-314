import os
import time
from typing import List
import cohere
from cohere.types.rerank_response import RerankResponse


def cohere_reranker(query: str, documents: List[str], top_n=4, retries=3) -> List[str]:
    try:
        cohere_client = cohere.Client(os.environ["COHERE_API_KEY"])
        reranked_response: RerankResponse = cohere_client.rerank(
            query=query, documents=documents, top_n=top_n, model="rerank-v3.5"
        )
        reranked_results = reranked_response.results
        reranked_documents = [documents[result.index] for result in reranked_results]
        return reranked_documents
    except Exception as e:
        print(e)
        if retries > 0:
            time.sleep(10)
            return cohere_reranker(
                query=query, documents=documents, top_n=top_n, retries=retries - 1
            )
