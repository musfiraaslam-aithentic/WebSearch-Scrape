import os
import json
import time
import random
import requests
from dotenv import load_dotenv
from tqdm import tqdm   # ✅ Progress bar

# --------------------------------------
# 1. Setup & Environment
# --------------------------------------
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")

if not API_KEY or not CSE_ID:
    raise ValueError("❌ GOOGLE_API_KEY or GOOGLE_CSE_ID not found in .env file.")

# Input / Output files
INPUT_FILE = "data.json"
OUTPUT_FILE = "google_results.json"

# --------------------------------------
# 2. Google Custom Search API Function
# --------------------------------------
def google_search(query, api_key=API_KEY, cse_id=CSE_ID, num_results=10):
    """Perform a Google Custom Search and return the top results."""
    service_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "num": num_results
    }
    response = requests.get(service_url, params=params, timeout=10)

    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    data = response.json()
    results = []
    for item in data.get("items", []):
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        })
    return results

# --------------------------------------
# 3. Processing Logic
# --------------------------------------
def process_json_file(input_file, output_file):
    """Read input JSON, perform Google search for each record, and save results."""
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    output = []
    total = len(data)
    print(f"📄 Found {total} records in {input_file}\n")

    # ✅ Use tqdm for progress visualization
    for i, entry in enumerate(tqdm(data, desc="🔍 Processing records", unit="record"), start=1):
        model = str(entry.get("MODEL", "") or "").strip()
        manufacturer = str(entry.get("MANUFACTURER", "") or "").strip()
        serial = str(entry.get("Serial Number", "") or "").strip()

        if not any([model, manufacturer, serial]):
            output.append({
                "index": i,
                "query": None,
                "results": [],
                "error": "No identifiable info"
            })
            continue

        query = " ".join(filter(None, [manufacturer, model, serial]))
        results, error = [], None

        for attempt in range(3):
            try:
                results = google_search(query)
                break
            except Exception as e:
                error = str(e)
                wait = 2 ** attempt + random.random()
                tqdm.write(f"⚠️ Attempt {attempt+1} failed for '{query}': {e}\n   Retrying in {wait:.1f}s...")
                time.sleep(wait)
        else:
            tqdm.write(f"❌ Failed after 3 attempts for: {query}")

        output.append({
            "index": i,
            "query": query,
            "results": results,
            "error": error
        })

        # Respect API rate limits
        time.sleep(1)

    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(output, out, indent=2, ensure_ascii=False)

    print(f"\n💾 All done! Saved {len(output)} entries to {output_file}")

# --------------------------------------
# 4. Main
# --------------------------------------
if __name__ == "__main__":
    process_json_file(INPUT_FILE, OUTPUT_FILE)
