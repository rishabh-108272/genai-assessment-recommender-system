import re

def normalize_url(url: str) -> str:
    """
    Normalize SHL URLs for evaluation matching
    """
    url = url.lower().strip()

    # remove protocol & domain
    url = re.sub(r"https?://www\.shl\.com", "", url)

    # remove trailing slash
    url = url.rstrip("/")

    return url
