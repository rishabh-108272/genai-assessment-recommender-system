import os
import requests
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HF_TOKEN = os.getenv("HF_API_KEY")

def query_embeddings(texts):
    if not HF_TOKEN:
        raise ValueError("HF_API_KEY not found. Check your .env file.")

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": texts,
        "options": {"wait_for_model": True}
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed ({response.status_code}): {response.text}")