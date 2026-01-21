# Local Setup (MVP)

This guide assumes local development with Next.js + FastAPI + Postgres.

## Prereqs

- Node.js 18+
- Python 3.11+
- Postgres 14+

## Environment

Create env files:

- `backend/.env`
- `frontend/.env.local`

### Backend env example

```
DATABASE_URL=postgresql://user:password@localhost:5432/email_audit
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
OAUTH_REDIRECT_URL=http://localhost:8000/api/auth/gmail/callback
TOKEN_ENCRYPTION_KEY=dev-key
```

### Frontend env example

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Run services

Backend:

```
cd backend
python -m venv .venv
. .venv/Scripts/Activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```
cd frontend
npm install
npm run dev
```

## Database

- Create a Postgres database named `email_audit`.
- Run migrations:

```
cd backend
alembic revision --autogenerate -m "init"
alembic upgrade head
```
