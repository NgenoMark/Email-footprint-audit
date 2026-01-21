# Privacy and Security (MVP)

This project is privacy-first. It only uses data the user explicitly grants
access to and stores the minimum required metadata.

## Core principles

- User-controlled access via OAuth.
- Minimal scopes (Gmail metadata read).
- No external account probing.
- Local-first storage.
- Simple data deletion path.

## Data handling

- Store only headers, metadata, and short snippets.
- Do not store full bodies by default.
- Encrypt OAuth tokens at rest.
- Allow users to wipe all local data.

## Threats and mitigations

- Token exposure: encrypt at rest and avoid logging secrets.
- Data leaks: never store raw message bodies unless needed.
- Over-scanning: use explicit user-triggered scans.
- Unauthorized access: require local auth (future).

## Future enhancements

- Per-user encryption keys.
- Fine-grained scope opt-in.
- Audit log for scans and exports.
