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
