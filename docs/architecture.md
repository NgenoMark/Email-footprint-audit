# Architecture (MVP)

This document outlines the MVP architecture for the Email Footprint Audit app.

## Overview

- Frontend: Next.js app for OAuth connect, dashboard, and evidence views.
- Backend: FastAPI API server handling OAuth, scans, and persistence.
- Data: Postgres for metadata, evidence, and service aggregation.
- Execution: Local first. All data stored on the user's machine.

## Components

### Frontend (Next.js)

- Pages: Connect, Dashboard, Service Detail, Settings.
- API client: typed helpers for backend calls.
- UI: list of services with confidence and evidence count.

### Backend (FastAPI)

- OAuth controller for Gmail connect and token refresh.
- Scan engine that runs Gmail queries, pulls headers/snippets.
- Service detection and confidence scoring pipeline.
- Export endpoint for CSV/JSON.

### Storage (Postgres)

- Users and connected accounts.
- Evidence emails with extracted signals.
- Services and evidence links.
- Scan run tracking.

## Data flow

1. User connects Gmail via OAuth.
2. Backend stores encrypted tokens in Postgres.
3. User triggers a scan.
4. Backend runs Gmail searches and stores evidence emails.
5. Detection pipeline groups evidence into services and scores confidence.
6. Frontend pulls service list and evidence details.

## Boundary decisions

- No external probing of websites.
- No storage of full email bodies in MVP.
- Minimal OAuth scopes (read-only metadata).

## Deployment (MVP)

- Local development: Next.js dev server + FastAPI on localhost.
- Production: optional Docker Compose for local run.
