from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict

from sarthakai.models import Chunk
from sarthakai.genai.tasks import reformat_table

CHUNK_SIZE = 500


def recursive_chunking(
    document_text: str, file_source: str = "", metadata: Dict = None
) -> List[Chunk]:
    metadata = metadata or {}
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    chunk_texts = text_splitter.create_documents([document_text])
    return [
        Chunk(text=chunk_text.page_content, file_source=file_source, metadata=metadata)
        for chunk_text in chunk_texts
    ]


def trim_llm_messages_history(messages, max_length=4096):
    if len("".join([str(message["content"]) for message in messages])) > max_length:
        messages = messages[1:]
        return trim_llm_messages_history(messages)
    else:
        return messages


def extract_tables_from_markdown_text(
    md_document: str, reformat_tables_with_llm: bool = False
):
    lines = md_document.splitlines()
    tables = []
    table = []
    non_table_text = []
    consecutive_pipe_lines = 0
    min_consecutive_lines = (
        3  # Minimum number of consecutive lines with pipes to classify as a table
    )

    for line in lines:
        # Check if the line contains a pipe symbol (|), indicating a potential table row
        if "|" in line:
            table.append(line)
            consecutive_pipe_lines += 1
        else:
            # If no pipe in line and we had a few consecutive table lines, consider it a complete table
            if consecutive_pipe_lines >= min_consecutive_lines:
                tables.append("\n".join(table))
            # Reset for the next potential table
            table = []
            consecutive_pipe_lines = 0
            # Add non-table lines to the text
            non_table_text.append(line)

    # If we end with a table and it's valid, append it
    if consecutive_pipe_lines >= min_consecutive_lines:
        tables.append("\n".join(table))

    # Rejoin non-table text into a single string
    non_table_text_str = "\n".join(non_table_text).strip()

    if reformat_tables_with_llm:
        tables = [reformat_table(table_to_reformat=table) for table in tables]
    return tables, non_table_text_str
