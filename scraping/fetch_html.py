# HTML Fetcher (Firecrawl-first)
# Responsibilities:
# - Input: list of top URLs (3 recommended) from JSON
# - Output: raw HTML for each URL, saved as JSON, readme and .html files

import json
import os
import time
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()
API = os.getenv("FIRECRAWL_API_KEY")


FIRECRAWL_ENDPOINT = "https://api.firecrawl.dev/v2/scrape"
INPUT_PATH = \
    "/Users/musfiraaslam/Documents/GitHub/websearchh/WebSearch-Scrape/testing/scraping/inputs/html_urls.json"
OUTPUT_DIR = \
    "/Users/musfiraaslam/Documents/GitHub/websearchh/WebSearch-Scrape/testing/scraping/outputs"
RESULTS_JSON = os.path.join(OUTPUT_DIR, "html_results.json")


def firecrawl_fetch(url: str, api_key: str, timeout_seconds: int = 30) -> Dict[str, Optional[str]]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "url": url,
        # Request markdown in addition to raw html when available
        "formats": ["markdown"]
    }
    try:
        resp = requests.post(FIRECRAWL_ENDPOINT, json=payload, headers=headers, timeout=timeout_seconds)
        if 200 <= resp.status_code < 300:
            html: Optional[str] = None
            markdown: Optional[str] = None
            if resp.headers.get("content-type", "").startswith("application/json"):
                data = resp.json()
                if isinstance(data, dict):
                    # Firecrawl may return these fields depending on plan/settings
                    html = data.get("html") or data.get("rawHtml") or data.get("content")
                    markdown = data.get("markdown") or data.get("md")
            if not html:
                html = resp.text
            # Some responses may embed JSON as a string under html; extract markdown if present
            if markdown is None and isinstance(html, str):
                stripped = html.strip()
                if stripped.startswith("{") and stripped.endswith("}"):
                    try:
                        embedded = json.loads(stripped)
                        # Support both top-level and nested under data
                        markdown = embedded.get("markdown")
                        if markdown is None and isinstance(embedded.get("data"), dict):
                            markdown = embedded["data"].get("markdown")
                    except Exception:
                        pass
            return {
                "url": url,
                "status": "success",
                "status_code": resp.status_code,
                "html": html,
                "markdown": markdown,
                "error": None,
            }
        return {
            "url": url,
            "status": "error",
            "status_code": resp.status_code,
            "html": None,
            "markdown": None,
            "error": f"Firecrawl HTTP {resp.status_code}: {resp.text[:300]}",
        }
    except requests.exceptions.RequestException as exc:
        return {
            "url": url,
            "status": "error",
            "status_code": None,
            "html": None,
            "markdown": None,
            "error": str(exc),
        }


def save_html_results_to_json(path: str, results: List[Dict[str, Optional[str]]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(results, f, indent=2)


def save_individual_html_files(output_dir: str, results: List[Dict[str, Optional[str]]]) -> List[str]:
    os.makedirs(output_dir, exist_ok=True)
    saved: List[str] = []
    for idx, r in enumerate(results, start=1):
        if r.get("status") == "success" and r.get("html"):
            path = os.path.join(output_dir, f"page_{idx}.html")
            with open(path, "w", encoding="utf-8") as f:
                f.write(r["html"])  # raw HTML
            saved.append(path)
    return saved


def save_individual_markdown_files(output_dir: str, results: List[Dict[str, Optional[str]]]) -> List[str]:
    os.makedirs(output_dir, exist_ok=True)
    saved: List[str] = []
    for idx, r in enumerate(results, start=1):
        if r.get("status") == "success" and r.get("markdown"):
            path = os.path.join(output_dir, f"page_{idx}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(r["markdown"])  # markdown view
            saved.append(path)
    return saved


if __name__ == "__main__":
    api_key = API
    if not api_key:
        raise ValueError("Missing FIRECRAWL_API_KEY in environment. Add it to your .env or export it.")

    with open(INPUT_PATH, "r") as f:
        data = json.load(f)

    urls_field = data.get("urls")
    if isinstance(urls_field, list):
        urls = [u for u in urls_field if isinstance(u, str) and u.strip()]
    elif isinstance(urls_field, str):
        urls = [urls_field]
    else:
        raise ValueError("Input JSON must contain 'urls' as a list or string.")

    # Take top 3
    urls = urls[:3]

    results: List[Dict[str, Optional[str]]] = []
    for idx, url in enumerate(urls):
        # Delay between requests
        time.sleep(1.0 + 0.25 * idx)
        result = firecrawl_fetch(url, api_key=api_key, timeout_seconds=30)
        results.append(result)

    save_html_results_to_json(RESULTS_JSON, results)
    files = save_individual_html_files(OUTPUT_DIR, results)
    md_files = save_individual_markdown_files(OUTPUT_DIR, results)

    print(f"Saved JSON results to: {RESULTS_JSON}")
    if files:
        print("Saved HTML files:")
        for p in files:
            print(f" - {p}")
    else:
        print("No HTML files saved (no successful fetches).")
    if md_files:
        print("Saved Markdown files:")
        for p in md_files:
            print(f" - {p}")