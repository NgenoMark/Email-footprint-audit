import csv
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.orm import Session

from app.db.models.service_alias import ServiceAlias


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


def load_domain_map(db: Session | None = None) -> dict[str, tuple[str, str | None]]:
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
    if db is not None:
        aliases = db.query(ServiceAlias).all()
        for alias in aliases:
            mapping[alias.domain.strip().lower()] = (
                alias.service_name,
                alias.category,
            )
    return mapping


def upsert_override(
    db: Session, domain: str, service_name: str, category: str | None
) -> None:
    target = domain.strip().lower()
    if not target or not service_name.strip():
        raise ValueError("Domain and service name are required")
    existing = db.query(ServiceAlias).filter_by(domain=target).first()
    if existing:
        existing.service_name = service_name.strip()
        existing.category = category
    else:
        db.add(
            ServiceAlias(
                domain=target, service_name=service_name.strip(), category=category
            )
        )
    db.commit()


def list_overrides(db: Session) -> list[dict[str, str]]:
    aliases = db.query(ServiceAlias).order_by(ServiceAlias.domain.asc()).all()
    return [
        {
            "domain": alias.domain,
            "service_name": alias.service_name,
            "category": alias.category or "",
        }
        for alias in aliases
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
