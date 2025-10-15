import os
import time
import json
import re
from datetime import datetime, timezone
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    default_headers={"Groq-Model-Version": "latest"}
)

USAGE_LOG_PATH = "usage_log.json"
DAILY_LIMIT = 250

def load_usage():
    """Load API usage tracking file."""
    if os.path.exists(USAGE_LOG_PATH):
        with open(USAGE_LOG_PATH, "r") as f:
            return json.load(f)
    return {}

def save_usage(usage_data):
    """Save usage count per day."""
    with open(USAGE_LOG_PATH, "w") as f:
        json.dump(usage_data, f)

def check_and_update_usage():
    """Increment usage counter, prevent exceeding daily limit."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    usage = load_usage()

    count = usage.get(today, 0)
    if count >= DAILY_LIMIT:
        print(f"⚠️ Daily limit of {DAILY_LIMIT} reached for {today}. No more requests allowed.")
        return False

    usage[today] = count + 1
    save_usage(usage)
    print(f"ℹ️ API calls today: {usage[today]} / {DAILY_LIMIT}")
    return True

def sanitize_filename(name: str) -> str:
    """Make a safe filename by replacing spaces and removing invalid characters."""
    safe_name = re.sub(r"[^\w\-]+", "_", name.strip())
    return safe_name[:100] 

def query_with_compound(query: str, model: str, instructions: str, output_path: str) -> str:
    """Runs one LLM query and writes the result to output_path."""
    if not check_and_update_usage():
        print("Aborting query due to daily limit reached.")
        return ""

    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": query}
    ]

    print(f"\n🔍 Processing Query: {query}\n")
    start_time = time.time()

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
    )

    content = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
            content += delta

    print(f"\n⏱️ Took {time.time() - start_time:.2f} seconds")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

    print(f"✅ Saved to: {output_path}\n")
    return content.strip()

def process_queries_file(filename="queries.txt", output_dir="results", skip_existing=True):
    """
    Reads each query from queries.txt, builds search string,
    sends to LLM, and saves each result as a Markdown file.
    """
    if not os.path.exists(filename):
        print(f"❌ File '{filename}' not found.")
        return

    os.makedirs(output_dir, exist_ok=True)

    with open(filename, "r", encoding="utf-8") as f:
        queries = [line.strip() for line in f if line.strip()]

    total = len(queries)
    for i, raw_query in enumerate(queries, start=1):
        query = f"{raw_query}"

        instructions = (
            f"Search for {raw_query}\n"
            "Provide the specifications\n"
            "Provide the References (URLs) used for search\n"
            "Give the response in structured format\n"
        )

        safe_name = sanitize_filename(raw_query)
        output_path = os.path.join(output_dir, f"{safe_name}.md")

        if skip_existing and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"⏩ Skipping existing file: {output_path}")
            continue

        print(f"\n({i}/{total}) Running query: {raw_query}")
        query_with_compound(query, "groq/compound", instructions, output_path)

        time.sleep(10)

# ---------- Run ----------
if __name__ == "__main__":
    process_queries_file("queries.txt", output_dir="groq_results", skip_existing=True)
