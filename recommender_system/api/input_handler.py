from query_understanding import understand_query
from pinecone_retriever import PineconeRetriever
from reranker import rerank_candidates
from domain_mapper import normalize_domains

# -----------------------------
# Configuration
# -----------------------------
RETRIEVAL_N = 200   # deep retrieval
TOP_K = 10           # final output

retriever = PineconeRetriever()


def process_input(query: str):
    """
    Full inference pipeline:
    Query → Understanding → Retrieval → Rerank → Output (Mapped to JSON Schema)
    """
    if not query or not query.strip():
        raise ValueError("Empty input query")

    # 1️⃣ Query understanding
    llm_output = understand_query(query)
    normalized_query = llm_output["normalized_query"]
    domains = normalize_domains(llm_output.get("domains", []))

    # 2️⃣ Vector retrieval
    candidates = retriever.retrieve(
        normalized_query,
        top_n=RETRIEVAL_N
    )

    # 3️⃣ Re-ranking (Pass domains as requested)
    reranked = rerank_candidates(
        query=normalized_query,
        candidates=candidates,
        domains=domains
    )

    # 4️⃣ Map to requested JSON format
    # Limit to TOP_K and transform keys to match the provided image schema
    final_output = []
    for item in reranked[:TOP_K]:
        transformed_item = {
            "url": item.get("URL"),
            "name": item.get("Test Solution"),
            "adaptive_support": item.get("adaptive_support"),
            "description": item.get("Description"),
            "duration": item.get("duration"),
            "remote_support": item.get("remote_support"),
            "test_type": item.get("test_type")
        }
        final_output.append(transformed_item)

    # Return the final structured dictionary
    return {"recommended_assessments": final_output}