from .embedding_utils import get_model
import numpy as np 

def embed_query(normalized_query: str)-> np.ndarray:
    # print("Please hang tight, embedding model is loading......")
    model=get_model()
    # print("Embedding model loaded successfully...")
    vec=model.encode(
        [normalized_query],
        normalize_embeddings=True
    )
    return vec 

