import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ServiceMatch:
    display_name: str
    category: str | None
    matched_domain: str
    match_type: str  # exact | subdomain | unknown


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _domain_map_paths() -> list[Path]:
    root = _repo_root()
    return [
        root / "data" / "domain_map" / "base_domains.csv",
        root / "data" / "domain_map" / "overrides.csv",
    ]


def load_domain_map() -> dict[str, tuple[str, str | None]]:
    mapping: dict[str, tuple[str, str | None]] = {}
    for path in _domain_map_paths():
        if not path.exists():
            continue
        with path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                domain = (row.get("domain") or "").strip().lower()
                name = (row.get("service_name") or "").strip()
                category = (row.get("category") or "").strip() or None
                if not domain or not name:
                    continue
                mapping[domain] = (name, category)
    return mapping


def upsert_override(domain: str, service_name: str, category: str | None) -> None:
    target = domain.strip().lower()
    if not target or not service_name.strip():
        raise ValueError("Domain and service name are required")
    override_path = _domain_map_paths()[1]
    override_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    if override_path.exists():
        with override_path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                rows.append(row)
    else:
        rows = []

    updated = False
    for row in rows:
        if (row.get("domain") or "").strip().lower() == target:
            row["service_name"] = service_name.strip()
            row["category"] = category or ""
            updated = True
            break

    if not updated:
        rows.append(
            {"domain": target, "service_name": service_name.strip(), "category": category or ""}
        )

    with override_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["domain", "service_name", "category"])
        writer.writeheader()
        writer.writerows(rows)


def list_overrides() -> list[dict[str, str]]:
    override_path = _domain_map_paths()[1]
    if not override_path.exists():
        return []
    with override_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [
            {
                "domain": (row.get("domain") or "").strip(),
                "service_name": (row.get("service_name") or "").strip(),
                "category": (row.get("category") or "").strip(),
            }
            for row in reader
            if row.get("domain") and row.get("service_name")
        ]


def resolve_service(domain: str, mapping: dict[str, tuple[str, str | None]]) -> ServiceMatch:
    target = domain.lower()
    best_domain = ""
    for mapped_domain in mapping.keys():
        if target == mapped_domain or target.endswith("." + mapped_domain):
            if len(mapped_domain) > len(best_domain):
                best_domain = mapped_domain
    if best_domain:
        name, category = mapping[best_domain]
        match_type = "exact" if target == best_domain else "subdomain"
        return ServiceMatch(
            display_name=name,
            category=category,
            matched_domain=best_domain,
            match_type=match_type,
        )
    return ServiceMatch(
        display_name=domain,
        category=None,
        matched_domain=domain,
        match_type="unknown",
    )
