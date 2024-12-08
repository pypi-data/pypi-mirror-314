import json
import os
from dotenv import load_dotenv
import nest_asyncio
from typing import List, Dict

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
import asyncio
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.readers.file import FlatReader
from pathlib import Path
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from llama_index.core.schema import Document

from utils.prompts import json_parsing_system_prompt
from utils.llm import (
    llm_call,
    async_llm_call,
    num_tokens_from_messages,
    split_string_before_m,
)
from document_parsing_from_file import *
from post_processing import *
from pre_processing import *

# from tqdm.notebook import tqdm

load_dotenv()
nest_asyncio.apply()
CHUNK_SIZE_LIMIT = 1000


async def convert_any_doc_to_md(filename, by_page=False):
    """Takes a locally saved pdf or excel file and calls teh respective function convert it into markdown"""
    if filename.endswith(".pdf"):
        all_documents_md = llamaparse_pdf_to_md(filename, by_page=by_page)
    elif (
        filename.endswith(".xls")
        or filename.endswith(".xlsx")
        or filename.endswith(".xlsm")
    ):
        all_documents_md = llamaparse_xls_to_md(filename, by_page=by_page)
    else:
        return False, []
    return True, all_documents_md


async def chunk_any_doc(filename, file_url):
    """First converts any locally saved doc to markdown and then chunks it."""
    print("Processing", filename)
    status, all_documents_md = await convert_any_doc_to_md(
        filename=filename, by_page=True
    )
    chunks = await chunk_md(all_documents_md, file_url)
    return status, chunks


async def chunk_md(all_documents_md: List, file_url, pages_are_separate=False):
    """Chunks a list of markdown documents chunks it using langchain text splitter."""
    chunks = []
    for document in all_documents_md:
        md_docs = Document(text=document["text"], metadata={})
        parser = MarkdownNodeParser()
        nodes = parser.get_nodes_from_documents([md_docs])
        text_chunks = breakdown_text_to_size_limit(nodes, CHUNK_SIZE_LIMIT)
        chunks += [
            {
                "text": remove_pipes_from_excel_md(text_chunk),
                "page_no": 1 if pages_are_separate else document["page_no"],
                "file_url": file_url,
            }
            for text_chunk in text_chunks
        ]
    return chunks


def breakdown_text_to_size_limit(nodes, text_size_limit):
    """Uses langchain recursive text splitter to first split the text on "\n", and then if it's still to large, by "\n"
    Until all resulting documents fit the required size limit."""
    chunks = []
    regular_text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=text_size_limit,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
    )
    text_splitter = RecursiveCharacterTextSplitter(
        # custom separators can be defined here using `separators=[...]`
        chunk_size=text_size_limit,
        chunk_overlap=50,
        length_function=len,
    )
    for node in nodes:
        if len(node.text) > text_size_limit:
            text = remove_spaces_between_newlines(node.text)
            texts = text_splitter.create_documents([text])
            chunks += [text.page_content for text in texts]
        else:
            chunks.append(node.text)
    return chunks
