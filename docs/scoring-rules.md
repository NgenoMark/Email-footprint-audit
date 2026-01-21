# Scoring Rules (MVP)

This document defines the initial confidence scoring for detected services.
Scoring is rule-based and deterministic for the MVP.

## Evidence types

Strong indicators:
- welcome
- verify
- reset
- receipt
- login
- otp

Helpful indicators:
- newsletter
- support
- profile_update
- billing_update

## Confidence bands

High:
- Official domain match + strong indicator + 2+ messages
- Official domain match + 2+ strong indicators

Medium:
- Official domain match + 1 strong indicator
- Official domain match + 1 strong + 1 helpful

Low:
- Only helpful indicators
- Only generic email providers (sendgrid, mailchimp) without brand confirmation

## Domain confidence

- Official domain match: from_domain matches known service domain.
- Likely domain match: subdomain of known domain (e.g., mail.netflix.com).
- Generic sender: common email platforms without brand hints.

## Notes

- Confidence is assigned per service, not per email.
- Evidence count is used to strengthen confidence, not reduce it.
- Rules may be replaced with a scoring model after MVP.
