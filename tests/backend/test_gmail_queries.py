from app.services.import_parsers import parse_password_manager_csv
from app.utils.parsing import classify_evidence_type


def test_classify_security_alert_as_login() -> None:
    assert classify_evidence_type("Security alert: new login") == "login"


def test_parse_bitwarden_like_csv() -> None:
    csv_text = "name,login_uri,username,password\nInstagram,https://instagram.com,a,b\n"
    domains = parse_password_manager_csv(csv_text)
    assert "instagram.com" in domains


def test_parse_fallback_csv() -> None:
    csv_text = "site,label\nhttps://github.com,GitHub\n"
    domains = parse_password_manager_csv(csv_text)
    assert domains == ["github.com"]
