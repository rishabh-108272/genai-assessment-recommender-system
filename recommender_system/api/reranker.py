from boosting import lexical_boost, url_boost
from duration_utils import extract_duration_constraint
from duration_scoring import duration_score
from domain_mapper import belongs_to_domain # Import the helper

def rerank_candidates(
    query: str,
    candidates: list,
    domains: list = None,  # Added domains parameter
    alpha: float = 0.30,   # Semantic
    beta: float = 0.40,    # Lexical
    gamma: float = 0.10,   # URL boost
    delta: float = 0.05,   # Duration
    epsilon: float = 0.15  # Domain weight (new)
):
    """
    Rerank candidates using weighted scores including Domain alignment.
    """
    target_duration = extract_duration_constraint(query)
    reranked = []
    
    # Ensure domains is a list
    query_domains = domains if domains else []

    for c in candidates:
        emb_score = c["score"]
        title_score = max(lexical_boost(query, c.get("Test Solution", "")), 0.0)
        url_score = url_boost(query, c.get("URL", ""))

        # 1. Duration scoring
        dur_score = 0.0
        if target_duration:
            dur_score = duration_score(c.get("duration"), target_duration)
        
        # 2. Domain scoring (New logic)
        # If any of the query's domains match the candidate's test types
        dom_score = 0.0
        if query_domains:
            # Check if candidate belongs to any of the domains found in the query
            matches = [belongs_to_domain(c, d) for d in query_domains]
            dom_score = 1.0 if any(matches) else 0.0

        # Adjust weights dynamically if optional signals are missing
        current_dur_weight = delta if target_duration else 0.0
        current_dom_weight = epsilon if query_domains else 0.0

        final_score = (
            alpha * emb_score +
            beta * title_score +
            gamma * url_score +
            current_dur_weight * dur_score +
            current_dom_weight * dom_score
        )

        c_new = dict(c)
        c_new["final_score"] = final_score
        c_new["domain_match"] = dom_score # Useful for debugging
        reranked.append(c_new)

    reranked.sort(key=lambda x: x["final_score"], reverse=True)
    return reranked