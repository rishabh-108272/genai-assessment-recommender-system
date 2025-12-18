from lexical_utils import tokenize

def lexical_boost(query: str, title: str) -> float:
    q_tokens = tokenize(query)
    t_tokens = tokenize(title)

    if not q_tokens or not t_tokens:
        return 0.0

    overlap = q_tokens & t_tokens
    return len(overlap) / len(q_tokens)

def url_boost(query: str, url: str) -> float:
    q_tokens = tokenize(query)

    # extract slug from URL
    slug = url.rstrip("/").split("/")[-1]
    slug_tokens = tokenize(slug.replace("-", " "))

    if not q_tokens or not slug_tokens:
        return 0.0

    overlap = q_tokens & slug_tokens
    return len(overlap) / len(q_tokens)
