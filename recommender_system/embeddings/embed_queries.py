from .embedding_utils import get_embeddings

def embed_query(normalized_query: str):
    """
    Generates an embedding for the query using Pinecone Inference API.
    Returns a list of floats (vector).
    """
    # No more local model loading or numpy processing
    vec = get_embeddings(normalized_query)
    
    # Pinecone Inference returns a list by default, 
    # which is exactly what the Pinecone retriever needs.
    return vec