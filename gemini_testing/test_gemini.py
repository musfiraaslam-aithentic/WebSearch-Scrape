import os
from google import genai
import re

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
# api key: AIzaSyBsUJfo6NsvKMSpy6MLNPt5TEK-giQcWr0

client = genai.Client()

# Path to your queries file
queries_file = "queries.txt"

# Function to make a safe filename from query
def safe_filename(name):
    # Remove or replace characters not allowed in filenames
    filename = re.sub(r'[\\/:"*?<>|]+', "_", name) + ".md"
    
    # Return full path in the results folder
    return os.path.join("results", filename)

# Read queries
with open(queries_file, "r", encoding="utf-8") as f:
    queries = [line.strip() for line in f if line.strip()]

# Loop through queries
for query in queries:
    print(f"Processing query: {query}")
    
    prompt = f"""Search for {query}
    Provide the specifications
    Provide the References (URLs) used for search
    Give the response in structured format"""
    
    # Call Gemini API
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"tools": [{"google_search": {}}]},
    )
    
    # Save response to file
    filename = safe_filename(query)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Query: {query}\n\n")
        f.write(response.text)
    
    print(f"Saved response to {filename}")
    
