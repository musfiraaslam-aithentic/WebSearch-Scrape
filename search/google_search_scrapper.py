import os
import json
import time
import random
import requests
from dotenv import load_dotenv
from tqdm import tqdm

# --------------------------------------
# 1. Setup & Environment
# --------------------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")

if not API_KEY or not CSE_ID:
    raise ValueError("❌ GOOGLE_API_KEY or GOOGLE_CSE_ID not found in .env file.")

INPUT_FILE = "data.json"
OUTPUT_FILE = "google_results.json"

# --------------------------------------
# 2. Helper: Clean up noisy text
# --------------------------------------
def clean_text(text):
    """Remove unwanted tokens or filler words."""
    if not text:
        return ""
    noise_words = ["manufacturer", "unknown", "code", "none", "null", "to be filled by o.e.m."]
    for word in noise_words:
        text = text.replace(word, "")
    return text.strip()

# --------------------------------------
# 3. Google Search Function
# --------------------------------------
def google_search(query, api_key=API_KEY, cse_id=CSE_ID, num_results=10):
    service_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "num": num_results,
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
# 4. Process File
# --------------------------------------
def process_json_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    output = []
    print(f"📄 Found {len(data)} records in {input_file}\n")

    for i, entry in enumerate(tqdm(data, desc="🔍 Searching Google", unit="entry"), start=1):
        # Build query
        model = clean_text(str(entry.get("MODEL", "") or ""))
        manufacturer = clean_text(str(entry.get("MANUFACTURER", "") or ""))
        serial = clean_text(str(entry.get("Serial Number", "") or ""))

        if not any([model, manufacturer, serial]):
            output.append({
                "index": i,
                "query": None,
                "results": [],
                "error": "No identifiable info"
            })
            continue

        # Create full and simplified queries
        query_full = " ".join(filter(None, [manufacturer, model, serial]))
        query_simple = " ".join(filter(None, [manufacturer, model]))

        results, error = [], None

        for attempt in range(3):
            try:
                results = google_search(query_full)
                if not results:
                    # Retry with simplified query if first query failed
                    results = google_search(query_simple)
                if results:
                    break
            except Exception as e:
                error = str(e)
                tqdm.write(f"⚠️ Error on attempt {attempt+1} for '{query_full}': {e}")
                time.sleep(2 ** attempt)
        
        if not results:
            tqdm.write(f"❌ No results found for: {query_full}")
        
        output.append({
            "index": i,
            "query": query_full,
            "results": results,
            "error": error
        })

        # Add randomized delay between queries (helps avoid rate limits)
        time.sleep(random.uniform(1.5, 3.5))

    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(output, out, indent=2, ensure_ascii=False)

    print(f"\n✅ Done! Saved {len(output)} entries to {output_file}")

# --------------------------------------
# 5. Main
# --------------------------------------
if __name__ == "__main__":
    process_json_file(INPUT_FILE, OUTPUT_FILE)
