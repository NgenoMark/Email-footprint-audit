from app.services.confidence_scoring import score_confidence


def test_high_confidence_with_official_and_multiple_strong() -> None:
    confidence, reason = score_confidence(["welcome", "receipt"], True)
    assert confidence == "high"
    assert "official domain" in reason


def test_medium_without_official_domain() -> None:
    confidence, _ = score_confidence(["welcome"], False)
    assert confidence == "medium"


def test_low_without_useful_signals() -> None:
    confidence, _ = score_confidence(["other"], False)
    assert confidence == "low"
