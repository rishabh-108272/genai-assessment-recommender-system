import numpy as np
# Import the function instead of get_model
from .embedding_utils import query_embeddings 

def embed_query(normalized_query: str) -> np.ndarray:
    # 1. Get the list of floats from the API
    raw_vec = query_embeddings([normalized_query])
    
    # 2. Convert to a NumPy array
    vec = np.array(raw_vec, dtype=np.float32)
    
    # 3. Manual Normalization (to replicate normalize_embeddings=True)
    norm = np.linalg.norm(vec, axis=1, keepdims=True)
    normalized_vec = vec / norm
    
    return normalized_vec