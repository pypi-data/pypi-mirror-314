# Utils
import os
import time
from typing import List

# Webscraping
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from firecrawl import FirecrawlApp
from googleapiclient.discovery import build

from sarthakai.models import WebSearchResponse


def get_webpage_content(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string if soup.title else ""
        text_content = " ".join(soup.stripped_strings)
        return True, f"{title}\n{text_content}"
    except requests.exceptions.RequestException as e:
        return False, e


def scrape_website_firecrawl(url: str, retries: int = 5, timeout: int = 30):
    app = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_API_KEY"))
    try:
        scrape_result = app.scrape_url(
            url=url,
            params={"formats": ["markdown"], "timeout": timeout},
        )
        return scrape_result
    except Exception as e:
        print(e)
        if retries > 0:
            return scrape_website_firecrawl(url=url, retries=retries - 1)
        else:
            return {"error": True}


def web_search_ddg(search_term: str, max_results: int = 5) -> List[WebSearchResponse]:
    raw_search_results = DDGS().text(search_term, max_results=max_results)
    web_search_results = [
        WebSearchResponse(
            url=search_result["href"],
            title=search_result["title"],
            snippet=search_result["body"],
        )
        for search_result in raw_search_results
    ]
    return web_search_results


def web_search_google(
    search_term: str, max_results: int = 5, **kwargs
) -> List[WebSearchResponse]:
    google_api_key = os.environ["GOOGLE_API_KEY"]
    google_cse_id = os.environ["GOOGLE_CSE_ID"]
    service = build("customsearch", "v1", developerKey=google_api_key)
    raw_search_results = (
        service.cse().list(q=search_term, cx=google_cse_id, **kwargs).execute()
    )
    if "items" not in raw_search_results.keys():
        return []
    raw_search_results = raw_search_results["items"][:max_results]
    web_search_results = [
        WebSearchResponse(
            url=search_result["link"],
            title=search_result["title"],
            snippet=search_result["snippet"],
        )
        for search_result in raw_search_results
    ]
    return web_search_results


def search_web_within_limited_domains(
    web_search_function,
    search_term: str,
    allowed_domains: List[str] = None,
    max_results: int = 5,
) -> List[WebSearchResponse]:
    search_results = []
    search_term_with_domains = f"{search_term} " + " OR ".join(
        [f"site:{domain}" for domain in allowed_domains]
    )
    search_results = web_search_function(
        search_term=search_term_with_domains, max_results=max_results
    )
    return search_results
