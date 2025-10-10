import os
import json
import time
import requests
from dotenv import load_dotenv

# ==============================================
# STEP 1: Load environment variables
# ==============================================
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")

if not API_KEY or not CSE_ID:
    raise ValueError("❌ Missing Google API Key or CSE ID. Please check your .env file.")

# ==============================================
# STEP 2: Google Custom Search Function
# ==============================================
def google_search(query, api_key, cse_id, num_results=3):
    """Perform Google Custom Search and return top results"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": num_results
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"⚠️ Google Search failed for query: {query}")
        print(f"Response: {response.text}")
        return []

    results = response.json().get("items", [])
    return [
        {
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        }
        for item in results
    ]

# ==============================================
# STEP 3: Main logic - Read data.json & process
# ==============================================
def process_json_file(input_file, output_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    results_output = []
    for entry in data:
        model = entry.get("MODEL")
        manufacturer = entry.get("MANUFACTURER")
        serial_number = entry.get("Serial Number")

        # Require both MODEL and MANUFACTURER; otherwise skip with a message
        if not model or not manufacturer:
            print(f"⚠️ Skipping entry {entry.get('entity_id')} - Missing MODEL or MANUFACTURER.")
            continue

        # Build query string
        search_terms = " ".join(
            [str(term) for term in [manufacturer, model, serial_number] if term and term != "null"]
        ).strip()

        if not search_terms:
            print(f"⚠️ Skipping entry {entry.get('entity_id')} - No valid search terms.")
            continue

        print(f"🔍 Searching for: {search_terms}")
        top_results = google_search(search_terms, API_KEY, CSE_ID)

        # Add to result file
        results_output.append({
            "entity_id": entry.get("entity_id"),
            "search_query": search_terms,
            "results": top_results
        })

        time.sleep(2)  # Be polite to the API and avoid rate limits

    # Write results to output file
    with open(output_file, "w") as out:
        json.dump(results_output, out, indent=4)
    print(f"\n✅ Results saved to {output_file}")


if __name__ == "__main__":
    input_file = "/Users/musfiraaslam/Documents/GitHub/websearchh/WebSearch-Scrape/testing/search/inputs/victus.json"          # File you uploaded earlier
    output_file = "/Users/musfiraaslam/Documents/GitHub/websearchh/WebSearch-Scrape/testing/search/outputs/victus_results.json"
    process_json_file(input_file, output_file)
