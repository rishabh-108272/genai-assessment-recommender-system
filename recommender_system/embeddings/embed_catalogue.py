import json
import numpy as np
from embedding_utils import get_model

def build_embedding_text(assessment: dict) -> str:
    # Extract fields with default values to prevent KeyErrors
    name = assessment.get("Test Solution", "N/A")
    test_types = assessment.get("Test Type(s)", [])
    description = assessment.get("Description", "No description available.")
    duration = assessment.get("Duration", "unknown duration")
    
    # Format the test types list into a string
    test_type_text = ", ".join(test_types) if isinstance(test_types, list) else str(test_types)
    
    # Construct a rich descriptive string for the embedding model
    embedding_text = (
        f"Assessment Name: {name}. "
        f"This is an SHL Individual assessment of type(s): {test_type_text}. "
        f"Estimated completion time: {duration}. "
        f"Description: {description}"
    )
    
    return embedding_text

def embed_catalogue(catalogue_path, output):
    
    with open(catalogue_path,"r",encoding="utf-8") as f:
        catalogue=json.load(f)
    
    texts=[build_embedding_text(a) for a in catalogue]
    
    model=get_model()
    embeddings=model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )
    
    np.save(output,embeddings)
    
    print(f"Embedded {len(texts)} assessments")
    return catalogue

catalogues=embed_catalogue("./shl_detailed_catalog.json","./catalogue_embeddings.npy")
print(catalogues)
