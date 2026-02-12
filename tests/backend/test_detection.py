from app.utils.domain_map import resolve_service


def test_resolve_service_exact_match() -> None:
    mapping = {"instagram.com": ("Instagram", "social")}
    match = resolve_service("instagram.com", mapping)
    assert match.display_name == "Instagram"
    assert match.match_type == "exact"


def test_resolve_service_subdomain_match() -> None:
    mapping = {"instagram.com": ("Instagram", "social")}
    match = resolve_service("mail.instagram.com", mapping)
    assert match.display_name == "Instagram"
    assert match.match_type == "subdomain"


def test_resolve_service_unknown_match() -> None:
    mapping = {}
    match = resolve_service("unknown.example", mapping)
    assert match.display_name == "unknown.example"
    assert match.match_type == "unknown"
