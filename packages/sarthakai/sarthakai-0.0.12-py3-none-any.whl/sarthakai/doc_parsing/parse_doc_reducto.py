import os
import requests
from typing import List

from sarthakai.genai.tasks import describe_table
from sarthakai.models import Chunk
from sarthakai.vector_search.common_utils import get_embedding_batch


def reducto_file_to_chunks(
    document_url: str, summarise_tables: bool = True, retries=5
) -> List[Chunk]:
    url = "https://platform.reducto.ai/parse"
    payload = {
        "document_url": document_url,
        "options": {"table_summary": {"enabled": summarise_tables}},
        "advanced_options": {"table_output_format": "md", "merge_tables": True},
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {os.environ['REDUCTO_API_KEY']}",
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()["result"]
        if result["type"] == "url":
            response = requests.get(result["url"])
            result = response.json()
        parsed_document = result["chunks"]
    except Exception as e:
        print("ERROR IN REDUCTO", e, response.text)
        if retries:
            return reducto_file_to_chunks(
                document_url=document_url,
                summarise_tables=summarise_tables,
                retries=retries - 1,
            )
        else:
            return []

    all_document_chunks = []
    print("Reducto finished parsing document. Now preparing chunks.")
    for chunk in parsed_document:
        vectorisable_chunk_content = ""
        unvectorisable_chunk_content = ""
        chunk_bounding_boxes = []
        page_numbers = set()
        current_page_number = 0
        for block in chunk["blocks"]:
            try:
                current_page_number = block["bbox"]["page"]
            except KeyError:
                print(block["bbox"].keys())
                pass
            page_numbers.add(current_page_number)
            chunk_bounding_boxes.append(block["bbox"])
            if block["type"] == "Table":
                table_content = block["content"]
                vectorisable_chunk_content += describe_table(
                    table_to_describe=table_content
                )
                unvectorisable_chunk_content += table_content
            else:
                vectorisable_chunk_content += block["content"]
                unvectorisable_chunk_content += block["content"]

        chunk = Chunk(
            text=unvectorisable_chunk_content,
            bounding_boxes=chunk_bounding_boxes,
            file_source=document_url,
            page_numbers=list(page_numbers),
            embedding=get_embedding_batch([vectorisable_chunk_content])[0],
        )
        all_document_chunks.append(chunk)
    return all_document_chunks
