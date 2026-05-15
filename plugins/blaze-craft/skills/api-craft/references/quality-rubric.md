# api-craft — Quality Rubric

Use this rubric on PR review of any API change or before claiming any contract work done.

## Verification matrix

| # | Check | Result |
|---|-------|--------|
| 1 | OpenAPI 3.1 / GraphQL schema committed and reflects the change. | pass / fail |
| 2 | Linter (Spectral or equivalent) returns zero errors on the spec. | pass / fail |
| 3 | A real client (curl or SDK) successfully calls every changed endpoint. | pass / fail |
| 4 | Response validates against the OpenAPI schema (response-validator middleware or post-hoc tool). | pass / fail |
| 5 | `meta` envelope present with `source`, `fetched_at`, `timezone` (or the documented equivalent). | pass / fail |
| 6 | Error path returns problem+json with a `code` from the controlled vocabulary. | pass / fail |
| 7 | Error vocabulary documented; new codes added to the canonical list. | pass / fail / n/a |
| 8 | Pagination walked end-to-end (first → next via cursor → past-end empty page). | pass / fail / n/a |
| 9 | `Link: <next-url>; rel="next"` header returned for paginated responses. | pass / fail / n/a |
| 10 | Idempotency-key replay verified: same body → cached response; different body → 409. | pass / fail / n/a |
| 11 | Rate-limit headers (`X-RateLimit-Limit`, `-Remaining`, `-Reset`) on every response. | pass / fail / n/a |
| 12 | `Retry-After` present on every 429. | pass / fail / n/a |
| 13 | Webhook payload signed (HMAC-SHA256 over timestamp + body); verifies on consumer. | pass / fail / n/a |
| 14 | Webhook retry policy documented (max attempts, backoff, jitter, dead-letter). | pass / fail / n/a |
| 15 | Webhook timestamp tolerance enforced (replay protection). | pass / fail / n/a |
| 16 | Auth credential in header (never query string). | pass / fail |
| 17 | Versioning strategy explicit; this change classified additive or breaking. | pass / fail |
| 18 | Deprecated endpoints carry `Deprecation: true` and `Sunset: <date>` headers. | pass / fail / n/a |
| 19 | Docs render from the spec (not hand-written), examples execute against staging. | pass / fail |
| 20 | Backward compatibility preserved within the major version. | pass / fail |

## Definition of done

A real client calling the API gets a predictable, schema-valid, documented response — and the
error path is just as predictable as the success path. Build success is not done. 200 from
the handler is not done. The contract-specific states below all need to hold:

- **Spec committed** — OpenAPI 3.1 / GraphQL schema in the repo, lint-clean, reflects this
  change.
- **Wire-verified** — a real client call against staging returns the documented shape.
- **Error path** — failure returns problem+json with a `code` from the controlled vocabulary
  and the HTTP status matches the semantic.
- **Headers present** — pagination links, rate-limit headers, idempotency echo, webhook
  signature.
- **Webhook contract honored** — signed, retried with backoff + jitter, dead-lettered,
  replay-protected.
- **Backward compatible within major** — no breaking changes inside a major version;
  deprecations carry `Sunset` and a migration path.
- **Docs live** — OpenAPI rendered, examples execute against staging.

Plus the cross-cutting baseline:

- Verification actually happened — evidence captured (curl transcript, linter output, schema
  validation result, signed webhook delivery log).
- Rollback plan exists (deprecate the new shape, sunset header set, previous version still
  honored for the deprecation window).

## Failure modes that block "done"

- The spec is committed but the handler returns a different shape.
- The error path returns a string body or a different envelope than the documented
  problem+json.
- Pagination "works" but the cursor is opaque-looking (base64) yet actually contains the
  offset (forces the same change set to consumers later when you switch to a real cursor).
- Idempotency-key replay returns success on different bodies (silent data loss).
- Webhook deliveries land but the signature scheme isn't documented anywhere — consumers
  can't verify them.
- Breaking change shipped in a minor version because "no public consumer is using it yet" —
  internal consumers count.
- Docs render but the curl example doesn't actually run.
