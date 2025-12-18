import json 
import numpy as np
import os 
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

# Configuration
EMBEDDINGS_PATH = './embeddings/catalogue_embeddings.npy'
CATALOGUE_PATH = './embeddings/shl_detailed_catalog.json'
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")  # Ensure this is in your env vars
INDEX_NAME = "shl-assessment-index"

def build_pinecone_index():
    # 1. Load Data
    embeddings = np.load(EMBEDDINGS_PATH).astype("float32")
    with open(CATALOGUE_PATH, "r", encoding="utf-8") as f:
        catalogue = json.load(f)
    
    dim = embeddings.shape[1]
    
    # 2. Initialize Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # 3. Create Index (if it doesn't exist)
    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=dim,
            metric='cosine', # Or 'dotproduct' depending on your embedding model
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )

    index = pc.Index(INDEX_NAME)

    # 4. Prepare Vectors for Upsert
    # Pinecone expects (id, vector, metadata)
    vectors_to_upsert = []
    for i, (vec, meta) in enumerate(zip(embeddings, catalogue)):
        vectors_to_upsert.append({
            "id": f"item_{i}", 
            "values": vec.tolist(), 
            "metadata": meta # Pinecone stores metadata alongside the vector
        })

    # 5. Batch Upsert (Recommended for efficiency)
    batch_size = 100
    for i in range(0, len(vectors_to_upsert), batch_size):
        index.upsert(vectors=vectors_to_upsert[i:i + batch_size])

    print(f"Pinecone index '{INDEX_NAME}' updated with {len(vectors_to_upsert)} assessments.")

if __name__ == "__main__":
    if not PINECONE_API_KEY:
        print("Please set your PINECONE_API_KEY environment variable.")
    else:
        build_pinecone_index()