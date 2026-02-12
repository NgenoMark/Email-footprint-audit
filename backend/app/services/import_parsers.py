import csv
import io
from urllib.parse import urlparse


def extract_domain(raw: str) -> str | None:
    if not raw:
        return None
    value = raw.strip()
    if not value:
        return None
    if "://" not in value:
        value = "https://" + value
    parsed = urlparse(value)
    return parsed.hostname.lower() if parsed.hostname else None


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace(" ", "_")


def _headers(reader: csv.DictReader) -> set[str]:
    return {_normalize_key(h) for h in (reader.fieldnames or [])}


def parse_password_manager_csv(text: str) -> list[str]:
    reader = csv.DictReader(io.StringIO(text))
    headers = _headers(reader)

    if {"login_uri", "username", "password"} <= headers:
        return _parse_bitwarden_rows(reader)
    if {"url", "username", "password"} <= headers:
        return _parse_generic_url_rows(reader)
    if {"website", "name"} <= headers:
        return _parse_generic_website_rows(reader)

    # Fallback parser: try common URL-like columns.
    return _parse_fallback_rows(reader)


def _parse_bitwarden_rows(reader: csv.DictReader) -> list[str]:
    domains: list[str] = []
    for row in reader:
        domain = extract_domain(row.get("login_uri", ""))
        if domain:
            domains.append(domain)
    return domains


def _parse_generic_url_rows(reader: csv.DictReader) -> list[str]:
    domains: list[str] = []
    for row in reader:
        domain = extract_domain(row.get("url", ""))
        if domain:
            domains.append(domain)
    return domains


def _parse_generic_website_rows(reader: csv.DictReader) -> list[str]:
    domains: list[str] = []
    for row in reader:
        domain = extract_domain(row.get("website", ""))
        if domain:
            domains.append(domain)
    return domains


def _parse_fallback_rows(reader: csv.DictReader) -> list[str]:
    domains: list[str] = []
    candidates = ("url", "uri", "website", "login_uri", "login_url", "site")
    for row in reader:
        for key in candidates:
            value = row.get(key)
            if not value:
                continue
            domain = extract_domain(value)
            if domain:
                domains.append(domain)
                break
    return domains
