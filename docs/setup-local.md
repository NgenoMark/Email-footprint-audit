# Local Setup Guide

This guide explains how to run Email Footprint Audit locally on a fresh machine.

## 1) Prerequisites

Install:

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Git
- Optional: Redis (only if you want queue mode with RQ)

## 2) Clone the repository

```powershell
git clone https://github.com/NgenoMark/Email-footprint-audit.git
cd Email-footprint-audit
```

## 3) Backend setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e .
```

If editable install is not supported in your environment, use:

```powershell
pip install fastapi "uvicorn[standard]" sqlalchemy alembic "psycopg[binary]" python-dotenv cryptography google-auth google-auth-oauthlib google-api-python-client rq redis pytest
```

## 4) Frontend setup

In a second terminal:

```powershell
cd frontend
npm install
```

## 5) Configure environment files

### `backend/.env`

Copy from `backend/.env.example` and set your real values:

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

Generate token key:

```powershell
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### `frontend/.env.local`

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api
NEXT_PUBLIC_DEFAULT_USER_EMAIL=
```

## 6) Google OAuth configuration (Gmail)

1. Create/select project in Google Cloud Console.
2. Enable Gmail API.
3. Configure OAuth consent screen.
- In testing mode, add your Gmail account as a test user.
4. Create OAuth credentials (Web application).
5. Set redirect URI to:

```text
http://localhost:8000/api/auth/gmail/callback
```

6. Put client ID/secret into `backend/.env`.

## 7) Create DB and run migrations

Create Postgres DB `email_audit`, then:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD"
$env:DATABASE_URL = "postgresql+psycopg://postgres:your_password@localhost:5432/email_audit"
alembic upgrade head
alembic current
```

## 8) Run the app

### Backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD"
uvicorn app.main:app --reload
```

Backend URL: `http://127.0.0.1:8000`

### Frontend

```powershell
cd frontend
npm run dev
```

Frontend URL: `http://localhost:3000`

## 9) First run flow

1. Open `http://localhost:3000/connect`
2. Connect Gmail
3. Open dashboard
4. Run a scan
5. Review services and evidence
6. Use settings for export/import/history/domain overrides

## 10) Optional queue mode (RQ + Redis)

Set in `backend/.env`:

```env
USE_RQ=true
REDIS_URL=redis://localhost:6379/0
```

Start Redis, then worker:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD"
python -m app.worker
```

## 11) Troubleshooting

### `ModuleNotFoundError: No module named 'app'`

```powershell
$env:PYTHONPATH = "$PWD"
```

### `ModuleNotFoundError: No module named 'psycopg2'`

Use `postgresql+psycopg://...` in `DATABASE_URL`.

### Missing DB columns

```powershell
alembic upgrade head
```

### `/api/auth/gmail/start` says credentials not set

Check `backend/.env`, then restart backend.

### OAuth 403 access denied

Add your Gmail account as OAuth test user in Google Console.
