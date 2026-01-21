# Sample Outputs

This document shows example API outputs and dashboard entries.

## Service list (API)

```json
{
  "items": [
    {
      "id": "uuid-1",
      "display_name": "Netflix",
      "primary_domain": "netflix.com",
      "category": "streaming",
      "confidence": "high",
      "confidence_reason": "welcome + receipts from official domain",
      "first_seen_at": "2019-08-12T12:00:00Z",
      "last_seen_at": "2023-10-01T11:00:00Z",
      "evidence_count": 5
    },
    {
      "id": "uuid-2",
      "display_name": "Substack",
      "primary_domain": "substack.com",
      "category": "newsletters",
      "confidence": "medium",
      "confidence_reason": "verify email from official domain",
      "first_seen_at": "2021-03-02T12:00:00Z",
      "last_seen_at": "2022-06-10T10:00:00Z",
      "evidence_count": 1
    }
  ]
}
```

## Service detail (API)

```json
{
  "id": "uuid-1",
  "display_name": "Netflix",
  "primary_domain": "netflix.com",
  "category": "streaming",
  "confidence": "high",
  "confidence_reason": "welcome + receipts from official domain",
  "first_seen_at": "2019-08-12T12:00:00Z",
  "last_seen_at": "2023-10-01T11:00:00Z",
  "evidence": [
    {
      "id": "e-1",
      "from_address": "info@netflix.com",
      "subject": "Welcome to Netflix",
      "sent_at": "2019-08-12T12:00:00Z",
      "evidence_type": "welcome",
      "match_reason": "domain_match"
    },
    {
      "id": "e-2",
      "from_address": "billing@netflix.com",
      "subject": "Your Netflix receipt",
      "sent_at": "2019-09-12T12:00:00Z",
      "evidence_type": "receipt",
      "match_reason": "domain_match"
    }
  ]
}
```

## Dashboard snippet (UI)

```
Netflix — High
Evidence: Welcome to Netflix (2019-08-12), Billing receipts (5)

Substack — Medium
Evidence: Confirm your email (2021-03-02)
```
