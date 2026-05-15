---
description: Audit the API error envelope and controlled-vocabulary `code` set; converge to RFC 9457 problem+json.
---

Use the api-craft skill to audit error envelopes and migrate to RFC 9457 problem+json for:
$ARGUMENTS

Produce:

- **Current state inventory** — every error shape currently in use across the API surface.
  Group by similarity.
- **Target envelope** — RFC 9457 problem+json: `{ type, title, status, detail, code,
  instance }`. `Content-Type: application/problem+json`.
- **Controlled `code` vocabulary** — list of allowed values
  (`auth_required`, `auth_invalid`, `validation_failed`, `not_found`, `rate_limited`,
  `upstream_unavailable`, `internal_error`, plus domain-specific codes). Each code mapped to
  HTTP status.
- **Migration plan** — how the existing surface migrates to the new envelope (parallel ship
  for N days, content negotiation, then 410 the old shape).
- **OpenAPI integration** — the `Problem` schema added to components/schemas, referenced
  from every error response. Spectral rule rejecting any error response that doesn't
  reference it.
- **Verification** — every error path returns problem+json with a code from the vocabulary;
  schema validation passes.

Reference RFC 9457.
