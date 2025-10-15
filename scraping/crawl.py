import argparse
import json
import os
import time

import requests
from dotenv import load_dotenv


FIRECRAWL_CRAWL_ENDPOINT = "https://api.firecrawl.dev/v2/crawl"


def submit_crawl_job(api_key: str, target_url: str, prompt: str, limit: int = 10, only_main_content: bool = True) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "url": target_url,
        "sitemap": "include",
        "crawlEntireDomain": True,
        "limit": limit,
        "prompt": prompt,
        "scrapeOptions": {
            "onlyMainContent": only_main_content,
            "maxAge": 172800000,
            "parsers": [],
            "formats": ["markdown"],
        },
    }
    resp = requests.post(FIRECRAWL_CRAWL_ENDPOINT, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()


def poll_crawl_job(api_key: str, job_id: str, poll_interval_sec: float = 2.0, timeout_sec: int = 120) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    status_url = f"{FIRECRAWL_CRAWL_ENDPOINT}/{job_id}"
    start = time.time()
    while True:
        resp = requests.get(status_url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        status = (data.get("status") or data.get("state") or "").lower()
        if status in {"completed", "success", "succeeded", "finished", "done"}:
            return data
        if status in {"failed", "error"}:
            return data
        if time.time() - start > timeout_sec:
            return {"status": "timeout", "data": data}
        time.sleep(poll_interval_sec)


def main():
    parser = argparse.ArgumentParser(description="Run Firecrawl crawl with a prompt and get the result back")
    parser.add_argument("--url", required=True, help="Root URL to crawl (e.g. https://copilot.microsoft.com/)")
    parser.add_argument("--prompt", required=True, help="Instruction to run over crawled pages")
    parser.add_argument("--limit", type=int, default=10, help="Max number of pages to crawl")
    parser.add_argument("--output", default="", help="Optional path to save JSON result")
    parser.add_argument("--output-dir", default="", help="If set, save crawl_result.json and metadata.json here")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("Missing FIRECRAWL_API_KEY in environment. Add it to your .env or export it.")

    try:
        submission = submit_crawl_job(api_key, args.url, args.prompt, limit=args.limit)
    except requests.HTTPError as e:
        print(json.dumps({"status": "error", "message": f"submission failed: {e}", "body": getattr(e.response, "text", "")}, indent=2))
        return

    job_id = submission.get("jobId") or submission.get("id")
    if not job_id:
        # Some plans may return immediate data; if so, print it
        if args.output:
            with open(args.output, "w") as f:
                json.dump(submission, f, indent=2)
            print(f"Saved result to {args.output}")
        else:
            print(json.dumps(submission, indent=2))
        return

    result = poll_crawl_job(api_key, job_id)
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Saved result to {args.output}")
    else:
        print(json.dumps(result, indent=2))

    # Save full result and extracted metadata if requested
    if args.output_dir:
        try:
            os.makedirs(args.output_dir, exist_ok=True)
            full_path = os.path.join(args.output_dir, "crawl_result.json")
            with open(full_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            print(f"Saved full crawl JSON to {full_path}")

            metadata_items = _extract_all_metadata_dicts(result)
            meta_path = os.path.join(args.output_dir, "metadata.json")
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(metadata_items, f, indent=2)
            print(f"Saved extracted metadata to {meta_path}")
        except Exception as e:
            print(f"Failed to save outputs to directory: {e}")


if __name__ == "__main__":
    main()


def _extract_all_metadata_dicts(obj):
    results = []

    def _walk(node):
        if isinstance(node, dict):
            # If this node itself looks like a result item with metadata
            meta = node.get("metadata")
            if isinstance(meta, dict):
                results.append(meta)
            # Recurse into values
            for v in node.values():
                _walk(v)
        elif isinstance(node, list):
            for it in node:
                _walk(it)

    _walk(obj)
    return results