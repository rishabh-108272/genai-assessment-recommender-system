import re
from typing import Optional

def extract_duration_constraint(query: str) -> Optional[int]:
    """
    Returns duration in minutes if present, else None
    Examples:
      '40 minutes' -> 40
      '1 hour' -> 60
      '1-2 hour' -> 120
      'about an hour' -> 60
    """
    q = query.lower()

    # 1–2 hours
    range_match = re.search(r"(\d+)\s*-\s*(\d+)\s*hour", q)
    if range_match:
        return int(range_match.group(2)) * 60

    # X hour(s)
    hour_match = re.search(r"(\d+)\s*hour", q)
    if hour_match:
        return int(hour_match.group(1)) * 60

    # minutes
    min_match = re.search(r"(\d+)\s*min", q)
    if min_match:
        return int(min_match.group(1))

    # phrases
    if "about an hour" in q or "around an hour" in q:
        return 60

    return None
