import pandas as pd
from collections import defaultdict
import numpy as np
import time

from query_understanding import understand_query
from pinecone_retriever import PineconeRetriever
from reranker import rerank_candidates
from domain_mapper import normalize_domains
from name_utils import normalize_name, name_from_url

TOP_K = 10
RETRIEVAL_N = 150

def load_train_data(path="evaluation/training_dataset.csv"):
    """
    Load ground-truth training data.
    CSV format:
    Query, Assessment_url
    """
    df = pd.read_csv(path)
    gt = defaultdict(set)

    for _, row in df.iterrows():
        query = str(row["Query"]).strip()
        url = str(row["Assessment_url"]).strip()
        if query and url:
            gt[query].add(url)

    return gt


def evaluation_recall_at_10():
    gt = load_train_data()
    retriever = PineconeRetriever()

    recalls = []

    for query, relevant_urls in gt.items():
        # --- Query Understanding ---
        llm_output = understand_query(query)
        time.sleep(2)  # avoid overload

        normalized_query = llm_output["normalized_query"]
        print("Normalized Query is: ",normalized_query)
        print("\n")
        domains = normalize_domains(llm_output.get("domains", []))
        print("Domains extracted: ",domains)
        print("\n")
        # --- Retrieval ---
        candidates = retriever.retrieve(
            normalized_query,
            top_n=RETRIEVAL_N
        )

        # --- Re-ranking ---
        reranked = rerank_candidates(
            query=normalized_query,
            candidates=candidates,
            domains=domains
        )

       
        predicted_names = {
            normalize_name(item["Test Solution"])
            for item in reranked
            if "Test Solution" in item
        }
        
        print("Predicted names: ",predicted_names)
        print("\n")
        ground_truth_names = {
            name_from_url(url)
            for url in relevant_urls
        }
        
        print("ground_truth_names: ",ground_truth_names)
        print("\n")

        hits = len(predicted_names & ground_truth_names)
        recall = hits / len(ground_truth_names) if ground_truth_names else 0.0

        recalls.append(recall)

        print(f"Query: {query}")
        print(f"Recall@{TOP_K}: {recall:.3f}")
        print("-" * 60)

    mean_recall = float(np.mean(recalls)) if recalls else 0.0
    print(f"\nMean Recall@{TOP_K}: {mean_recall:.4f}")

    return mean_recall


if __name__ == "__main__":
    evaluation_recall_at_10()
