# Vision

Email Footprint Audit is a personal, permission-based tool to reconstruct the
services tied to your email address from evidence in your inbox. It helps users
reduce risk, find forgotten subscriptions, and clean up their digital footprint.

## Goals

- Discover services linked to a user email using inbox evidence.
- Provide a clear dashboard with confidence and evidence.
- Keep data local and private.
- Offer export and cleanup guidance.

## Non-goals

- Probing external sites to test account existence.
- Automated account deletion or password changes.
- Storing full email bodies by default.

## MVP success criteria

- Gmail OAuth connect works end to end.
- Inbox scan returns 30-200 likely services (varies by inbox).
- Services include evidence trails and confidence reasons.
- Export to CSV/JSON.
