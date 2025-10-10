import os
import time
import json
from datetime import datetime, timezone
from groq import Groq
from dotenv import load_dotenv

# ----- Load Environment Variables -----
load_dotenv()

# Initialize Groq client with compound model header
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    default_headers={
        "Groq-Model-Version": "latest"
    }
)

USAGE_LOG_PATH = "usage_log.json"
DAILY_LIMIT = 250

def load_usage():
    if os.path.exists(USAGE_LOG_PATH):
        with open(USAGE_LOG_PATH, "r") as f:
            return json.load(f)
    return {}

def save_usage(usage_data):
    with open(USAGE_LOG_PATH, "w") as f:
        json.dump(usage_data, f)

def check_and_update_usage():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")  # timezone-aware UTC
    usage = load_usage()

    count = usage.get(today, 0)
    if count >= DAILY_LIMIT:
        print(f"⚠️ Daily limit of {DAILY_LIMIT} reached for {today}. No more requests allowed.")
        return False

    usage[today] = count + 1
    save_usage(usage)
    calls_left = DAILY_LIMIT - usage[today]

    
    print(f"\nℹ️ API calls today ({today}): {usage[today]} / {DAILY_LIMIT} (Remaining: {calls_left})")
    if calls_left <= 10:
        print("⚠️ Warning: Approaching daily limit!")

    return True

def log_request_time():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    # print(f"🕒 Request made at: {now}")

def query_with_compound(query: str, model: str = "groq/compound", instructions: str = None, output_path: str = "compound_results.md") -> str:
    """Queries Groq's Compound model with a single prompt and writes only the result to a Markdown file."""

    if not check_and_update_usage():
        print("Aborting query due to daily limit reached.")
        return ""

    log_request_time()

    system_content = instructions or (
        "You are a helpful assistant that can use web search if needed. "
        "Answer the following query clearly and concisely in **Markdown** format. "
        "Include relevant data, sources, or specs if applicable."
    )

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": query}
    ]

    print(f"\n🔍 Processing Query...\n")
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

    print(f"\n⏱️ Took {time.time() - start_time:.2f} seconds\n")

    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

    print(f"✅ Result saved to: {output_path}\n")
    return content.strip()



if __name__ == "__main__":
    query = "Search for Inspiron 7472 and extract information about Model Name and Specifications."
    instructions = (
        "You are a research assistant. Use web search if needed to gather accurate, up-to-date information. "
        "Format results based strictly on queries and nothing more. Store results neatly in Markdown."
    )

    query_with_compound(
        query=query,
        model="groq/compound",
        instructions=instructions,
        output_path="compound_query_results.md"
    )
