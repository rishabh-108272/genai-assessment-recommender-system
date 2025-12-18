import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()
# Use a hosted model equivalent to MiniLM or better
# Examples: "multilingual-e5-large" or "relevance-semantic-v1"
MODEL_NAME = "multilingual-e5-large" 

_pc_client = None

def get_pinecone_client():
    global _pc_client
    if _pc_client is None:
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable is not set")
        _pc_client = Pinecone(api_key=api_key)
    return _pc_client

def get_embeddings(text: str):
    """
    Replaces the old SentenceTransformer local call with a Pinecone API call.
    """
    pc = get_pinecone_client()
    
    # Generate embedding using Pinecone's hosted inference
    response = pc.inference.embed(
        model=MODEL_NAME,
        inputs=[text],
        parameters={"input_type": "query"}
    )
    
    # Return the vector list
    return response[0].values