# Email Footprint Audit

Personal, permission-based tool to reconstruct the services tied to your email
address from evidence in your inbox. It scans for account signals, groups by
service, scores confidence, and shows a clean dashboard with evidence.

## Status

MVP scaffolded. Documentation-first phase in progress.

## Core features (MVP)

- Gmail OAuth connect (read-only metadata).
- Targeted inbox scan for account signals.
- Service detection and deduplication.
- Confidence scoring with evidence reasons.
- Dashboard + service detail views.
- Export to CSV/JSON.
- Local-first storage with Postgres.

## Architecture

- Frontend: Next.js (React + TypeScript).
- Backend: FastAPI (Python).
- Database: Postgres.

## Docs

- `docs/vision.md`
- `docs/architecture.md`
- `docs/privacy-security.md`
- `docs/data-model.md`
- `docs/api-contract.md`
- `docs/scoring-rules.md`
- `docs/sample-outputs.md`
- `docs/setup-local.md`

## Local setup (summary)

See `docs/setup-local.md` for full instructions.

## Repo layout

```
frontend/   Next.js UI
backend/    FastAPI API
docs/       Project docs/specs
data/       Domain maps and samples
infra/      Docker assets
tests/      Test suites
scripts/    Utility scripts
```
