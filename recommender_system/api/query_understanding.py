import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Recommended fast models: "llama-3.3-70b-versatile" or "llama-3.1-8b-instant"
MODEL_NAME = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
You are a hiring query analyzer.

Your job is to understand the hiring intent without losing semantic meaning.

Return ONLY valid JSON with the following fields:

1. normalized_query:
   - A clean, natural-language version of the original query
   - Preserve role, intent, context, and constraints
   - DO NOT compress into keywords
   - DO NOT shorten aggressively
   - This text will be used directly for semantic embeddings

2. domains:
   - List of assessment domains
   - Examples: ["Technical"], ["Behavioral"], ["Technical", "Behavioral"]

3. skills:
   - Explicit skills mentioned in the query
   - Example: ["Java", "SQL"]

4. seniority:
   - One of: "Intern", "Entry", "Mid", "Senior", "Leadership"
   - Or null if not specified

Important rules:
- Do NOT remove hiring intent
- Do NOT remove role context
- Do NOT output explanations or markdown
- Output JSON ONLY
"""


def understand_query(query: str) -> dict:
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        model=MODEL_NAME,
        # This ensures the model outputs valid JSON
        response_format={"type": "json_object"} 
    )
    
    # Extract the text content from the response
    content = chat_completion.choices[0].message.content
    return json.loads(content)

