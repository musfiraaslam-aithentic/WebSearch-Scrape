from groq import Groq
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import time

# ----- Load Environment Variables -----
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm_client = Groq(api_key=GROQ_API_KEY)


def refine_with_model(documents: list[str], model: str, instructions: str = None, output_path: str = "refined_results.md") -> list[str]:
    """Refines or summarizes a list of documents using Groq LLM and writes only the results to a Markdown file."""
    results = []

    for i, doc in enumerate(documents):
        system_content = instructions or (
            "You are a helpful assistant. Summarize and refine the following text clearly in Markdown.\n\n"
            "**Instructions:**\n"
            "- Keep only essential information.\n"
            "- Use **bold** for key terms.\n"
            "- Use bullet points or short paragraphs.\n"
            "- Do not include extra commentary."
        )

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": doc}
        ]

        print(f"\n🧠 Processing Document {i + 1}/{len(documents)}...\n")
        start_time = time.time()

        stream = llm_client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.5,
            max_completion_tokens=512,
            top_p=1,
            stream=True,
        )

        content = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                print(delta, end="", flush=True)
                content += delta

        print()
        results.append(content.strip())

        print(f"⏱️ Took {time.time() - start_time:.2f} seconds\n")

    
    with open(output_path, "w", encoding="utf-8") as f:
        for result in results:
            f.write(result + "\n")

    print(f"✅ Results saved to: {output_path}\n")
    return results



if __name__ == "__main__":
    
    # Parses HTML file
    with open("response.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Remove tags
    for tag in soup(["script", "style", "meta", "noscript", "link"]):
        tag.decompose()

    # Get text
    text = soup.get_text(separator="\n")

    
    clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

    # Send it to Groq LLM
    model = "llama-3.1-8b-instant"
    instructions = (
        "You are a precise summarizer. Read the provided text extracted from an HTML page. "
        "Extract and summarize data specifically about **model names** and their **specifications** in Markdown format."
    )

    refine_with_model([clean_text], model, instructions, output_path="summarized_html.md")
