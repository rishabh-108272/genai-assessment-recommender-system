import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables from .env
load_dotenv()

def query_embeddings(texts, model_id="sentence-transformers/all-MiniLM-L6-v2"):
    """
    Sends a list of texts to Hugging Face Inference API and returns embeddings.
    """
    api_key = os.getenv("HF_API_KEY")
    
    if not api_key:
        raise ValueError("HF_API_KEY not found. Please set it in your .env file.")

    # Initialize the client
    client = InferenceClient(api_key=api_key)

    try:
        # Generate embeddings
        # client.feature_extraction returns a list of lists (vectors)
        embeddings = client.feature_extraction(text=texts, model=model_id)
        return embeddings

    except Exception as e:
        print(f"Error fetching embeddings: {e}")
        return None