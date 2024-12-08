import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from llama_index.core.storage.storage_context import StorageContext

from llama_index.core import (
    Settings,
    ServiceContext,
    VectorStoreIndex,
    SimpleDirectoryReader,
)
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.schema import Document
from typing import List, Dict

from sarthakai.genai.tasks import route_query
from sarthakai.models import Chunk, VectorSearchResponse

from sarthakai.common import generate_random_id
from sarthakai.vector_search.common_utils import get_embedding_batch

load_dotenv()
CHUNK_SIZE = 100000

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))


def list_all_pinecone_indexes(to_return: str = "index_objects"):
    all_indexes = pc.list_indexes()
    if to_return == "index_objects":
        return all_indexes
    elif to_return == "names":
        return [index.name for index in all_indexes]


def list_all_namespaces_in_pinecone_index(pinecone_index_name: str):
    pinecone_index = pc.Index(pinecone_index_name)
    return list(pinecone_index.describe_index_stats()["namespaces"].keys())


def get_or_create_pinecone_index(pinecone_index_name: str, dimension=1536):
    """Create a new index on Pinecone.
    Set dimension = 3072 if using text-embedding-3-large, and 1536 for small."""
    try:
        pinecone_index = pc.Index(pinecone_index_name)
        return True, pinecone_index
    except:
        pc.create_index(
            name=pinecone_index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        pinecone_index = pc.Index(pinecone_index_name)
        return False, pinecone_index


def add_chunks_to_pinecone_index(
    pinecone_index_name, namespace_name, chunks: List[Chunk]
):
    """Add data into an existing Pinecone vectordb"""

    pinecone_index = pc.Index(pinecone_index_name)
    pinecone_index.upsert(
        namespace=namespace_name,
        vectors=[
            {
                "id": generate_random_id(),
                "values": chunk.embedding,
                "metadata": chunk.metadata_in_pinecone_format,
            }
            for chunk in chunks
        ],
    )

    """# Define which vectordb to use and how to chunk the docs
    vector_store = PineconeVectorStore(
        pinecone_index=pinecone_index, namespace=namespace_name
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    Settings.chunk_size = CHUNK_SIZE

    documents = []
    for chunk in chunks:
        documents.append(
            Document(
                # text=doc["text"],
                doc_id=generate_random_id(),
                extra_info=chunk.metadata,
            )
        )

    # Add data to the index
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, service_context=Settings
    )
    """


def route_query_to_relevant_pinecone_namespace(query: str, pinecone_index_name: str):
    all_namespace_names = list_all_namespaces_in_pinecone_index(
        pinecone_index_name=pinecone_index_name
    )
    route = route_query(query=query, routes=all_namespace_names)
    return route


def search_pinecone(
    pinecone_index_name: str,
    namespace_name: str,
    query: str,
    n_results: int = 4,
    distance_threshold: float = 10,
    embedding_model="text-embedding-3-small",
) -> List[VectorSearchResponse]:
    """Search Pinecone vectordb"""
    index = pc.Index(pinecone_index_name)
    query_embedding = get_embedding_batch(input_array=[query], model=embedding_model)
    raw_search_results = index.query(
        vector=query_embedding,
        namespace=namespace_name,
        top_k=n_results,
        include_metadata=True,
    )["matches"]

    # Format search results
    vector_search_responses = []
    for search_result in raw_search_results:
        distance = (
            1 - search_result["score"]
        )  # Pinecone returns a similarity score instead of distance
        if distance < distance_threshold:
            vector_search_response = VectorSearchResponse(
                document=search_result["metadata"]["text"],
                distance=distance,
                metadata=search_result["metadata"],
            )
            vector_search_responses.append(vector_search_response)

    return vector_search_responses


# pinecone_index.describe_index_stats()


def delete_pinecone_index(pinecone_index_name):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    try:
        pc.delete_index(pinecone_index_name)
    except Exception as e:
        print("The index", pinecone_index_name, "doesn't exist.", e)
