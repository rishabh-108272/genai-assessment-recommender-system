import re

def normalize_name(name: str) -> str:
    if not name: return ""
    name = str(name).lower()
    
    # Remove URL encoded characters like 28 ( ( ) and 29 ( ) )
    name = name.replace("28", " ").replace("29", " ")
    
    # Strip common artifacts that appear in URLs but not metadata
    noise = [
        r"\(new\)", r"\bnew\b", r"7\-1", r"7\-0", 
        r"solution", r"essentials", r"sift\sout"
    ]
    for pattern in noise:
        name = re.sub(pattern, "", name)
    
    # Remove all non-alphanumeric and extra spaces
    name = re.sub(r"[^a-z0-9]", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

def name_from_url(url: str) -> str:
    slug = url.rstrip("/").split("/")[-1]
    slug = slug.replace("-", " ")
    return normalize_name(slug)