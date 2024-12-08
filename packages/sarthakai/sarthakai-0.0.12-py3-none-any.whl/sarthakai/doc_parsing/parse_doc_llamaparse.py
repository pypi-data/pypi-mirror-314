import os
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv
import nest_asyncio

from sarthakai.doc_parsing.text_preprocessing import (
    extract_tables_from_markdown_text,
    recursive_chunking,
)
from sarthakai.genai.tasks import describe_table
from sarthakai.models import Chunk

nest_asyncio.apply()
load_dotenv()


def llamaparse_file_to_md(
    file_path: str, additional_parsing_instructions: str = "", by_page=False
):
    """Uses LlamaParse to parse a doc saved locally into a markdown string."""
    llamaparse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
    parser = LlamaParse(
        api_key=llamaparse_api_key,
        parsing_instruction=additional_parsing_instructions,
        result_type="markdown",  # "markdown" and "text" are available
    )
    # filetype = file_path.split(".")[-1]
    # file_extractor = {f".{filetype}": parser}
    documents = parser.load_data(file_path)

    if by_page:
        parsed_md_document = [
            {"text": document.text, "page_no": i + 1}
            for i, document in enumerate(documents)
        ]
    else:
        parsed_md_document = "".join([document.text for document in documents])
    return parsed_md_document


def parse_document_with_tables(document_file_path: str, document_filename: str):
    all_documents_chunks = []
    additional_parsing_instructions = "Parse the tables in a markdown format carefully so that no columns are empty and no headers are empty."

    parsed_md_document = llamaparse_file_to_md(
        file_path=document_file_path,
        additional_parsing_instructions=additional_parsing_instructions,
    )
    tables, remaining_parsed_md_document = extract_tables_from_markdown_text(
        md_document=parsed_md_document, reformat_tables_with_llm=True
    )
    print(len(tables), "tables detected.")
    for table in tables:
        table_description = describe_table(table)
        table_chunk = Chunk(
            text=table_description,
            non_vectorised_addendum_text=table,
            file_source=document_filename,
        )
        all_documents_chunks.append(table_chunk)
    chunks = recursive_chunking(
        document_text=remaining_parsed_md_document, file_source=document_filename
    )
    all_documents_chunks += chunks
    return all_documents_chunks
