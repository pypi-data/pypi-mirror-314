from typing import List, Dict
import chromadb
from chromadb.api.models import Collection
from slugify import slugify
from sarthakai.genai.tasks import route_query
from sarthakai.models import Chunk, VectorSearchResponse
from sarthakai.common import generate_random_id
from sarthakai.vector_search.common_utils import get_embedding_batch


def list_all_chromadb_collections(chromadir: str, to_return="collection_objects"):
    chromadb_client = chromadb.PersistentClient(path=chromadir)
    if to_return == "collection_objects":
        return chromadb_client.list_collections()
    elif to_return == "names":
        return [collection.name for collection in chromadb_client.list_collections()]


def get_or_create_chromadb_collection(chromadir: str, collection_name: str):
    chromadb_client = chromadb.PersistentClient(path=chromadir)
    print("Existing collections:", chromadb_client.list_collections())
    collection_name = slugify(collection_name)
    print("Looking for", collection_name)
    collection_already_exists = (
        True
        if collection_name in [c.name for c in chromadb_client.list_collections()]
        else False
    )
    print("collection_already_exists", collection_already_exists)
    # try:
    collection = chromadb_client.get_or_create_collection(name=collection_name)
    return collection_already_exists, collection
    """except:
        print("CRRRRATBAF")
        chromadb_client = chromadb.PersistentClient(path=chromadir)
        collection = chromadb_client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
            # embedding_function=openai_ef,
        )
        return False, collection"""


def add_chunks_to_chromadb_collection(chunks: List[Chunk], collection: Collection):
    print(f"Adding {len(chunks)} to {collection}")
    embeddings = (
        get_embedding_batch(input_array=[chunk.text for chunk in chunks])
        if not (all([chunk.embedding for chunk in chunks]))
        else [chunk.embedding for chunk in chunks]
    )
    collection.add(
        embeddings=embeddings,
        documents=[chunk.text for chunk in chunks],
        ids=[generate_random_id() for _ in range(len(chunks))],
        metadatas=[chunk.metadata_in_chromadb_format for chunk in chunks],
    )


def route_query_to_relevant_chromadb_collection(query: str, chromadir: str):
    all_collection_names = list_all_chromadb_collections(chromadir, to_return="names")
    route = route_query(query=query, routes=all_collection_names)
    return route


def search_chromadb(
    chromadir: str,
    collection_name: str,
    query: str,
    n_results: int = 4,
    distance_threshold: float = 3.0,
    metadata_constraints: Dict = None,
) -> List[VectorSearchResponse]:
    client = chromadb.PersistentClient(path=chromadir)
    collection = client.get_collection(collection_name)
    query_emb = get_embedding_batch([query])  # [0]
    raw_search_results = (
        collection.query(
            query_embeddings=query_emb,
            n_results=n_results,
            where=metadata_constraints,
        )
        if metadata_constraints
        else collection.query(
            query_emb,
            n_results=n_results,
        )
    )

    documents = raw_search_results["documents"][0]
    distances = raw_search_results["distances"][0]
    metadatas = raw_search_results["metadatas"][0]

    vector_search_responses = []
    for document, distance, metadata in zip(documents, distances, metadatas):
        if distance < distance_threshold:
            vector_search_response = VectorSearchResponse(
                document=document, distance=distance, metadata=metadata
            )
            vector_search_responses.append(vector_search_response)
    return vector_search_responses

    """seen_items = set()
    unique_results = [
        item
        for item in results
        if tuple(item.items()) not in seen_items
        and not seen_items.add(tuple(item.items()))
    ]
    return unique_results"""


def two_step_vector_search(
    query: str,
    chromadir_1: str,
    collection_name_1: str,
    chromadir_2: str,
    collection_name_2: str,
    distance_threshold_1: float = 0.25,
    distance_threshold_2: float = 0.30,
):
    context_documents = []
    articles_vector_search_responses = search_chromadb(
        chromadir=chromadir_1,
        collection_name=collection_name_1,
        query=query,
        distance_threshold=distance_threshold_1,
    )
    context_documents = [
        response.metadata["text"] for response in articles_vector_search_responses
    ]
    if not articles_vector_search_responses:
        chunks_vector_search_responses = search_chromadb(
            chromadir=chromadir_2,
            collection_name=collection_name_2,
            query=query,
            distance_threshold=distance_threshold_2,
        )
        context_documents = [
            response.document for response in chunks_vector_search_responses
        ]
    return context_documents
