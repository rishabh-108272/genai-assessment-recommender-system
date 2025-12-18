import os
import re
from pinecone import Pinecone
from recommender_system.embeddings.embed_queries import embed_query

# Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "shl-assessment-index"


def parse_duration(duration_str):
    """
    Converts '16 minutes' → 16
    """
    if not duration_str:
        return None

    match = re.search(r"(\d+)", str(duration_str))
    return int(match.group(1)) if match else None


class PineconeRetriever:
    def __init__(self):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.pc.Index(INDEX_NAME)

    def retrieve(self, normalized_query: str, top_n: int = 30):
        # 1. Generate query embedding
        query_vec = embed_query(normalized_query)
        query_vec = query_vec.tolist() if hasattr(query_vec, "tolist") else query_vec

        # 2. Query Pinecone
        response = self.index.query(
            vector=query_vec,
            top_k=top_n,
            include_metadata=True
        )

        results = []

        # 3. Normalize metadata strictly
        for match in response.get("matches", []):
            meta = match.get("metadata", {})

            item = {
                "Test Solution": meta.get("Test Solution"),
                "URL": meta.get("URL"),
                "Description": meta.get("Description", "").strip(),

                # Canonicalized fields
                "adaptive_support": meta.get("Adaptive/IRT", "No"),
                "remote_support": meta.get("Remote Testing", "No"),
                "duration": parse_duration(meta.get("Duration")),
                "test_type": meta.get("Test Type(s)", []),

                # Retrieval info
                "score": float(match.get("score", 0.0)),
                "id": match.get("id"),
            }

            # Safety filter: skip broken rows
            if item["URL"] and item["Test Solution"]:
                results.append(item)

        return results
