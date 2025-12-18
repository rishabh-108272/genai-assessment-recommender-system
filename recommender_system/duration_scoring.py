def duration_score(
    candidate_duration: int,
    target_duration: int,
    tolerance: int = 15
) -> float:
    """
    Soft duration score between 0 and 1.
    Full score if within tolerance.
    Linear decay beyond tolerance.
    """
    if candidate_duration is None:
        return 0.0

    diff = abs(candidate_duration - target_duration)

    if diff <= tolerance:
        return 1.0

    # soft decay
    return max(0.0, 1.0 - (diff / target_duration))
