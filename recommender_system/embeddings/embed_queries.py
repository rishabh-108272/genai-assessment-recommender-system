import numpy as np
from embeddings.embedding_utils import query_embeddings 

def embed_query(normalized_query: str) -> np.ndarray:
    # 1. Get the raw list from the API
    raw_results = query_embeddings([normalized_query])
    
    # FIX: Check if the API returned None or an empty list BEFORE conversion
    if raw_results is None or len(raw_results) == 0:
        raise ValueError("Failed to retrieve embeddings from API.")

    # 2. Extract the first vector and convert to NumPy
    vec = np.array(raw_results[0], dtype=np.float32)
    
    # 3. Manual Normalization
    norm = np.linalg.norm(vec)
    
    # Avoid division by zero if the vector is empty/zero
    if norm > 0:
        normalized_vec = vec / norm
    else:
        normalized_vec = vec
        
    return normalized_vec