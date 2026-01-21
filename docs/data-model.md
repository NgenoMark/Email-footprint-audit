# Data Model (Postgres, MVP)

This document defines the initial relational model used by the backend. It is
designed for the Gmail-only MVP and optimized for evidence traceability.

## Conventions

- IDs are UUIDs (generated in app layer).
- Timestamps are UTC and stored as `timestamptz`.
- Email bodies are not stored in MVP. Only metadata and short snippets.

## Tables

### users

Represents a local app user.

- id: uuid, pk
- email: text, unique, not null
- display_name: text, null
- created_at: timestamptz, not null
- updated_at: timestamptz, not null

### connected_accounts

Connected inbox accounts and tokens.

- id: uuid, pk
- user_id: uuid, fk -> users.id, not null
- provider: text, not null (gmail)
- provider_account_id: text, not null (gmail user id)
- access_token_enc: text, not null
- refresh_token_enc: text, not null
- scopes: text[], not null
- token_expires_at: timestamptz, null
- created_at: timestamptz, not null
- updated_at: timestamptz, not null

Unique: (provider, provider_account_id)

### services

Deduplicated services inferred from evidence emails.

- id: uuid, pk
- user_id: uuid, fk -> users.id, not null
- display_name: text, not null (Netflix)
- primary_domain: text, not null (netflix.com)
- category: text, null (streaming, finance, etc.)
- confidence: text, not null (high, medium, low)
- confidence_reason: text, not null (short explanation)
- first_seen_at: timestamptz, null
- last_seen_at: timestamptz, null
- created_at: timestamptz, not null
- updated_at: timestamptz, not null

Unique: (user_id, primary_domain)

### evidence_emails

Stored email metadata and extracted signals.

- id: uuid, pk
- user_id: uuid, fk -> users.id, not null
- provider: text, not null (gmail)
- provider_message_id: text, not null
- from_address: text, not null
- from_domain: text, not null
- subject: text, not null
- snippet: text, null
- sent_at: timestamptz, not null
- received_at: timestamptz, not null
- evidence_type: text, not null (welcome, verify, reset, receipt, login, otp, other)
- raw_headers: jsonb, null
- created_at: timestamptz, not null

Unique: (provider, provider_message_id)

### service_evidence_links

Many-to-many link between services and evidence.

- id: uuid, pk
- service_id: uuid, fk -> services.id, not null
- evidence_email_id: uuid, fk -> evidence_emails.id, not null
- match_reason: text, not null (domain_match, subject_brand, link_brand)
- created_at: timestamptz, not null

Unique: (service_id, evidence_email_id)

### scan_runs

Tracks scan operations for a user/account.

- id: uuid, pk
- user_id: uuid, fk -> users.id, not null
- connected_account_id: uuid, fk -> connected_accounts.id, not null
- status: text, not null (queued, running, success, failed)
- query: text, not null (gmail search string)
- started_at: timestamptz, null
- finished_at: timestamptz, null
- error_message: text, null
- created_at: timestamptz, not null

## Indexes

- evidence_emails(user_id, from_domain)
- evidence_emails(user_id, sent_at desc)
- services(user_id, confidence)
- service_evidence_links(service_id)
- service_evidence_links(evidence_email_id)
- scan_runs(user_id, status)
