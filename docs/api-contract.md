# API Contract (MVP)

Base URL: `/api`

All responses are JSON. Errors follow a standard envelope.

## Error format

```json
{
  "error": {
    "code": "validation_error",
    "message": "Human readable message"
  }
}
```

## Auth

MVP uses a local user record. OAuth flow is initiated by the frontend and
handled server-side. Session strategy is open for later decision.

## Endpoints

### Health

GET `/health`

Response
```json
{ "status": "ok" }
```

### OAuth: Gmail

GET `/auth/gmail/start`

Response
```json
{ "url": "https://accounts.google.com/o/oauth2/v2/auth?..." }
```

GET `/auth/gmail/callback`

Response
```json
{ "connected": true }
```

### Scans

POST `/scans`

Request
```json
{
  "provider": "gmail",
  "query": "subject:(welcome OR verify OR \"confirm your email\" OR \"password reset\" OR receipt OR invoice)"
}
```

Response
```json
{
  "scan_id": "uuid",
  "status": "queued"
}
```

GET `/scans`

Response
```json
{
  "items": [
    {
      "id": "uuid",
      "status": "running",
      "query": "subject:(welcome OR verify OR ...)",
      "started_at": "2024-01-01T12:00:00Z",
      "finished_at": null
    }
  ]
}
```

### Services

GET `/services`

Query params
- `q`: text search
- `confidence`: high | medium | low

Response
```json
{
  "items": [
    {
      "id": "uuid",
      "display_name": "Netflix",
      "primary_domain": "netflix.com",
      "category": "streaming",
      "confidence": "high",
      "confidence_reason": "welcome + receipts from official domain",
      "first_seen_at": "2019-08-12T12:00:00Z",
      "last_seen_at": "2023-10-01T11:00:00Z",
      "evidence_count": 5
    }
  ]
}
```

GET `/services/{serviceId}`

Response
```json
{
  "id": "uuid",
  "display_name": "Netflix",
  "primary_domain": "netflix.com",
  "category": "streaming",
  "confidence": "high",
  "confidence_reason": "welcome + receipts from official domain",
  "first_seen_at": "2019-08-12T12:00:00Z",
  "last_seen_at": "2023-10-01T11:00:00Z",
  "evidence": [
    {
      "id": "uuid",
      "from_address": "info@netflix.com",
      "subject": "Welcome to Netflix",
      "sent_at": "2019-08-12T12:00:00Z",
      "evidence_type": "welcome",
      "match_reason": "domain_match"
    }
  ]
}
```

### Evidence

GET `/evidence`

Query params
- `service_id`: uuid
- `type`: welcome | verify | reset | receipt | login | otp | other

Response
```json
{
  "items": [
    {
      "id": "uuid",
      "from_address": "no-reply@substack.com",
      "from_domain": "substack.com",
      "subject": "Confirm your email",
      "sent_at": "2021-03-02T12:00:00Z",
      "evidence_type": "verify",
      "snippet": "Click the button to confirm..."
    }
  ]
}
```

### Exports

POST `/exports`

Request
```json
{ "format": "csv" }
```

Response
```json
{ "url": "/exports/2024-01-01/services.csv" }
```

### Settings

POST `/settings/delete-data`

Response
```json
{ "deleted": true }
```
