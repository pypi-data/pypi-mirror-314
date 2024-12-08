import os
import time
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

# Initialize the ApifyClient with your Apify API token
apify_client = ApifyClient(os.environ["APIFY_TOKEN"])


def crawl_webpage_and_linked_pages_into_md(url: str):
    """Calls the Apify API to crawl a given link and return the processed webpages in markdown string format"""
    md_pages = []
    # Prepare the Actor input
    run_input = {
        "startUrls": [{"url": url}],
        "crawlerType": "playwright:adaptive",
        "includeUrlGlobs": [],
        "excludeUrlGlobs": [],
        "initialCookies": [],
        "proxyConfiguration": {"useApifyProxy": True},
        "removeElementsCssSelector": """nav, footer, script, style, noscript, svg,
    [role=\"alert\"],
    [role=\"banner\"],
    [role=\"dialog\"],
    [role=\"alertdialog\"],
    [role=\"region\"][aria-label*=\"skip\" i],
    [aria-modal=\"true\"]""",
        "clickElementsCssSelector": '[aria-expanded="false"]',
    }

    # Run the Actor and wait for it to finish
    run = apify_client.actor("apify/website-content-crawler").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    print(
        "💾 Check your data here: https://console.apify.com/storage/datasets/"
        + run["defaultDatasetId"]
    )
    for item in apify_client.dataset(run["defaultDatasetId"]).iterate_items():
        md_pages.append({"text": item["markdown"], "file_url": item["url"]})
    return md_pages


def get_google_reviews_apify(placeId, reviews_start_date=None, retries=3):
    false = False
    true = True
    run_input = {
        "deeperCityScrape": false,
        "includeWebResults": false,
        "language": "en",
        "maxImages": 0,
        "maxReviews": 2000,
        "oneReviewPerRow": true,
        "onlyDataFromSearchPage": false,
        "scrapeResponseFromOwnerText": true,
        "scrapeReviewId": true,
        "scrapeReviewUrl": true,
        "scrapeReviewerId": true,
        "scrapeReviewerName": true,
        "scrapeReviewerUrl": true,
        "searchStringsArray": ["place_id:" + placeId],
    }
    if reviews_start_date:
        run_input["reviewsStartDate"] = reviews_start_date
    google_reviews = []
    try:
        run = apify_client.actor("compass/crawler-google-places").call(
            run_input=run_input
        )
        for item in apify_client.dataset(run["defaultDatasetId"]).iterate_items():
            google_reviews.append(item)
    except Exception as e:
        time.sleep(600)
        retries -= 1
        if retries > 0:
            google_reviews = get_google_reviews_apify(placeId, reviews_start_date)
        else:
            print("ERRORs on apify:", e)
            return []
    return google_reviews
