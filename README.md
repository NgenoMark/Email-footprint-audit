# Email Footprint Audit

Email Footprint Audit is a personal, permission-based tool that helps a user discover which services are tied to their email address.

It works by scanning inbox evidence (welcome emails, verification emails, reset emails, receipts), grouping messages by service, scoring confidence, and showing results in a dashboard.

## What This Project Does

- Connects Gmail using OAuth.
- Scans Gmail for account and subscription evidence.
- Detects and deduplicates services.
- Scores confidence (high/medium/low) with evidence reasons.
- Shows services, evidence, scan history, queue health, and import history in the UI.
- Supports CSV/JSON exports.
- Stores data locally in Postgres.

## Tech Stack

- Frontend: Next.js 14 + React + TypeScript
- Backend: FastAPI + SQLAlchemy + Alembic
- Database: PostgreSQL
- Optional background jobs: RQ + Redis

## Repository Layout

```text
frontend/   Next.js application
backend/    FastAPI application
docs/       Specifications and architecture docs
data/       Domain mapping CSVs
tests/      Backend tests
```

## Prerequisites

Install these first:

1. Python 3.11+
2. Node.js 18+
3. PostgreSQL 14+
4. Git
5. (Optional) Redis, if you want queue mode (`USE_RQ=true`)

## Installation

### 1) Clone the repository

```powershell
git clone https://github.com/NgenoMark/Email-footprint-audit.git
cd Email-footprint-audit
```

### 2) Backend setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e .
```

If `pip install -e .` does not work in your environment, install dependencies directly:

```powershell
pip install fastapi "uvicorn[standard]" sqlalchemy alembic "psycopg[binary]" python-dotenv cryptography google-auth google-auth-oauthlib google-api-python-client rq redis pytest
```

### 3) Frontend setup

Open a second terminal:

```powershell
cd frontend
npm install
```

## Environment Configuration

### Backend env file

Create `backend/.env` from `backend/.env.example`.

Required keys:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/email_audit
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
OAUTH_REDIRECT_URL=http://localhost:8000/api/auth/gmail/callback
TOKEN_ENCRYPTION_KEY=your_generated_fernet_key
GOOGLE_SCOPES=https://www.googleapis.com/auth/gmail.readonly
FRONTEND_URL=http://localhost:3000
SESSION_COOKIE_NAME=efa_user_email
ALLOW_LEGACY_SINGLE_USER_FALLBACK=true
USE_RQ=false
REDIS_URL=redis://localhost:6379/0
```

Generate `TOKEN_ENCRYPTION_KEY` with:

```powershell
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### Frontend env file

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api
NEXT_PUBLIC_DEFAULT_USER_EMAIL=
```

## Google Gmail OAuth Setup

1. Go to Google Cloud Console.
2. Create/select a project.
3. Enable Gmail API.
4. Configure OAuth consent screen.
- For personal testing: keep app in Testing mode.
- Add your Gmail account under Test users.
5. Create OAuth credentials:
- Application type: Web application
- Authorized redirect URI: `http://localhost:8000/api/auth/gmail/callback`
6. Copy client ID and client secret into `backend/.env`.

## Database Setup

Create database `email_audit` in Postgres.

Then run migrations:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD"
$env:DATABASE_URL = "postgresql+psycopg://postgres:your_password@localhost:5432/email_audit"
alembic upgrade head
alembic current
```

## Run the Application

### Start backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD"
uvicorn app.main:app --reload
```

Backend API will run on `http://127.0.0.1:8000`.

### Start frontend

```powershell
cd frontend
npm run dev
```

Frontend will run on `http://localhost:3000`.

## First-Time Usage Flow

1. Open `http://localhost:3000/connect`.
2. Click Connect Gmail and complete OAuth.
3. Go to Dashboard.
4. Run a scan.
5. Review detected services and evidence.
6. Use Settings for exports, domain map overrides, and password manager import.

## Optional Queue Mode (RQ + Redis)

If you want queued scans:

1. Set in `backend/.env`:

```env
USE_RQ=true
REDIS_URL=redis://localhost:6379/0
```

2. Start Redis.
3. Start worker in a separate terminal:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD"
python -m app.worker
```

## Tests

Run backend tests:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "."
python -m pytest ..\tests\backend -q
```

## Common Issues and Fixes

### 1) `ModuleNotFoundError: No module named 'app'`

Set PYTHONPATH in backend terminal:

```powershell
$env:PYTHONPATH = "$PWD"
```

### 2) `ModuleNotFoundError: No module named 'psycopg2'`

Use `psycopg` URL scheme in `DATABASE_URL`:

```env
DATABASE_URL=postgresql+psycopg://...
```

### 3) Missing DB column errors (for example `cursor_before_sent_at`)

Run migrations:

```powershell
alembic upgrade head
```

### 4) `/api/auth/gmail/start` returns `GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET not set`

Make sure values exist in `backend/.env`, then restart backend.

### 5) Google OAuth `Error 403: access_denied`

Your Gmail account is not in OAuth Test users, or consent screen is not correctly configured.

## Security Notes

- Tokens are stored encrypted.
- Project is local-first for personal auditing.
- Do not commit `.env` files or secrets.

## Additional Docs

- `docs/vision.md`
- `docs/architecture.md`
- `docs/privacy-security.md`
- `docs/data-model.md`
- `docs/api-contract.md`
- `docs/scoring-rules.md`
- `docs/sample-outputs.md`
- `docs/setup-local.md`
