import re
from typing import Set

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "are",
    "who", "can", "also", "will", "about", "into", "want",
    "looking", "hire", "hiring", "role", "job", "position"
}

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str) -> Set[str]:
    tokens = set(normalize_text(text).split())
    return {t for t in tokens if t not in STOPWORDS and len(t) > 2}
