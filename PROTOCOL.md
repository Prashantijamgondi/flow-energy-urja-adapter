# PROTOCOL.md — How Urja Meter Ops Actually Works

This document records what I found by inspecting `https://urja-ops.flockenergy.tech` directly
in Chrome DevTools (Network tab, "Preserve log" enabled), rather than assuming how it works.

> Fill in each `[ ]` below after your own DevTools pass. Keep it factual — screenshots-in-words
> of the actual request/response are more valuable than prose.

## 1. Authentication

- Login URL: `[ TODO — e.g. POST /login or POST /api/auth/signin ]`
- Request method: `[ TODO — POST? ]`
- Payload shape: `[ TODO — form-encoded fields (username/password) or JSON body? field names exactly as sent ]`
- CSRF / anti-forgery token: `[ TODO — is there a hidden input or header token fetched from the login page first? ]`
- Successful response: `[ TODO — status code (200 vs 302), and whether Set-Cookie appears ]`
- Cookie name(s) set: `[ TODO — exact cookie name, e.g. session, sid, connect.sid ]`
- Cookie attributes: `[ TODO — HttpOnly? Secure? SameSite? Expiry? ]`
- Failure response (wrong password): `[ TODO — status code and body ]`
- Session expiry behavior: `[ TODO — what happens when you wait and then make a request with a stale cookie — 401? redirect to /login? ]`

## 2. Internal Endpoints Discovered

List every distinct request the frontend makes while you navigate (list, detail, consumption
pages). For each:

| Method | Path | Purpose | Response type |
|--------|------|---------|----------------|
| `[ ]`  | `[ ]` | `[ ]` | `[ JSON / HTML ]` |

Note whether the app is a server-rendered HTML app or a JS framework (SvelteKit, Next.js, etc.)
making calls to a JSON API under the hood — this changes the whole client design.

## 3. Data Structures

- Meter list shape: `[ TODO — fields present per meter: id, serial, status, location...]`
- Meter detail shape: `[ TODO ]`
- Consumption history shape: `[ TODO — granularity: hourly/daily? date format? units? ]`
- Hierarchy (if present): `[ TODO — how are meters grouped — feeder/DTR/substation? ]`

## 4. Anomalies & Quirks

- `[ TODO — missing fields, inconsistent date formats, pagination quirks, rate limits, N/A values, duplicate IDs, etc. ]`
