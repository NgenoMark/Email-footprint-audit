from collections import Counter


STRONG_TYPES = {"welcome", "verify", "reset", "receipt", "login", "otp"}
HELPFUL_TYPES = {"newsletter", "support", "profile_update", "billing_update"}


def score_confidence(evidence_types: list[str], official_domain: bool) -> tuple[str, str]:
    counts = Counter(evidence_types)
    strong = sum(counts[t] for t in STRONG_TYPES)
    helpful = sum(counts[t] for t in HELPFUL_TYPES)
    total = sum(counts.values())

    if official_domain and (strong >= 2 or (strong >= 1 and total >= 2)):
        return "high", "official domain + multiple strong indicators"
    if official_domain and strong >= 1:
        return "medium", "official domain + strong indicator"
    if official_domain and helpful >= 1:
        return "medium", "official domain + helpful indicator"
    if strong >= 1:
        return "medium", "strong indicator without confirmed domain"
    if helpful >= 1:
        return "low", "only helpful indicators"
    return "low", "insufficient evidence"
