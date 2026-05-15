# api-craft — Anti-Patterns

Push back when you see these. Each ships with a concrete fix path. Several of these are drawn
from the BSI surface specifically — they're the ones that bite production APIs.

## Contract shape

### Endpoints returning data without a `meta` envelope.

**Fix:** Wrap every response body in `{ data, meta }` where `meta` carries `source`,
`fetched_at`, and `timezone` at minimum. The consumer needs to know where the data came from
and how fresh it is to decide what to display. Bake this into the OpenAPI components/schemas as
a base envelope and reference it everywhere.

### Different error shapes per endpoint within the same API.

**Fix:** Adopt RFC 9457 problem+json across every error response. Document a controlled
vocabulary of `code` values (e.g. `auth_required`, `rate_limited`, `validation_failed`,
`upstream_unavailable`). One envelope, one vocabulary, one place to look up what each code
means.

### Status codes leaking into user-facing copy.

**Fix:** Status codes are for machines. Humans see plain language ("Sign in to continue", not
"401 Unauthorized"). The API can return whatever status code is semantically right; the UI
translates it. This belongs in the SDK / client layer, not the API.

## Versioning + compatibility

### Breaking changes shipped in a minor version.

**Fix:** A breaking change is anything that requires a working consumer to change its code to
keep working: removed field, semantic change to existing field, narrowed accepted enum values,
required field added, error code semantic change. Shipping any of these requires a major
version bump and a deprecation cycle on the previous version.

### Deprecations without a `Sunset` header or a sunset date.

**Fix:** Every deprecated endpoint returns a `Deprecation: true` and `Sunset: <RFC 9110 date>`
header. Pair with a `Link: <migration-doc-url>; rel="deprecation"`. Without a real sunset
date, deprecation is a wish; with one, consumers actually migrate.

### Versioning strategy chosen by accident (because somebody added `/v2/` once).

**Fix:** Pick a strategy on purpose: URI prefix (`/v2/`), `Accept-Version` header, or
media-type versioning (`application/vnd.org.v2+json`). Document why. URI is most operator-friendly
and CDN-friendly; header keeps URLs stable; media type is purest but breaks browser exploration.

## Pagination

### Pagination via offset on tables that change frequently.

**Fix:** Cursor pagination. Offset on a fast-changing collection causes skipped rows (insert
between fetches) and duplicated rows (delete between fetches). The cursor encodes the position
in a stable way (last-seen ID + sort key) so the consumer can keep walking even if the
collection mutates underneath.

### `total_count` returned on every page request.

**Fix:** Compute `total_count` only when explicitly requested (`?include=total_count`). The
COUNT(*) is often more expensive than the page itself, and most consumers don't actually need
it.

### `next_url` not provided; consumers have to construct it themselves.

**Fix:** Return `Link: <next-url>; rel="next"` (RFC 8288). The consumer follows the link
without knowing the API's pagination scheme — and the API can change its scheme later without
breaking any consumer.

## Idempotency + retries

### Idempotency-key replays succeed silently when the body differs from the original.

**Fix:** Same key + same body → return the cached response (idempotent retry). Same key +
different body → return 409 Conflict with a problem+json explaining "this key was used with a
different request". Silent success on body mismatch is a footgun that produces silent data
loss.

### 429 returned without `Retry-After`.

**Fix:** Always include `Retry-After` (seconds, or HTTP-date). The whole point of 429 is to
tell the client when it can try again. Without that header, the client retries immediately and
makes the situation worse.

### Idempotency-key has no replay window documented.

**Fix:** Document how long the key is honored (24h is common). After the window, the same key
is treated as a fresh request. Consumers need this to size their retry-cache logic.

## Rate limiting

### Rate-limit headers missing.

**Fix:** Return `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` on
**every** response (not just 429s). The whole point is for consumers to throttle themselves
proactively, not learn the limits by getting blocked.

### Rate limit scoped to IP only.

**Fix:** Scope to the API key (or user) primarily; IP only as a backstop against unauth abuse.
A shared NAT or office IP otherwise gets one user blocking many.

## Webhooks

### Webhook delivery without HMAC signatures.

**Fix:** Sign every webhook payload with HMAC-SHA256 over `timestamp + body`, send the
signature and timestamp as headers (`X-Signature: t=<ts>,v1=<hex>`). Consumer verifies
signature AND that timestamp is within a tolerance window (5 minutes). Without this, webhook
endpoints are open to anybody who guesses the URL.

### Webhook retries without exponential backoff + jitter.

**Fix:** Retry with exponential backoff (e.g. 1s → 2s → 4s → 8s …) plus random jitter (±25%)
to avoid thundering herd when many deliveries fail at once. Cap at a max attempt count (e.g.
8) and after that, send to a dead-letter queue.

### Webhook ordering claimed but not guaranteed.

**Fix:** HTTP delivery has no inherent ordering guarantee. Either add a sequence number to the
payload (consumer reconciles), use an ordered transport (Kafka, SQS FIFO), or document
explicitly that ordering is best-effort.

### Replay attacks possible because timestamp tolerance isn't checked.

**Fix:** Reject webhook deliveries whose timestamp is older than the tolerance window
(typically 5 minutes). Even with a valid signature, an attacker who captures a delivery can't
replay it later.

## Authentication

### API keys carried in query strings.

**Fix:** Always headers (`Authorization: Bearer <token>` or `X-API-Key: <key>`). Query strings
end up in CDN logs, browser history, server access logs, referrer headers — any of which can
leak the credential.

### Bearer tokens with no rotation policy.

**Fix:** Document rotation cadence (e.g. 90 days), how the consumer rotates, what happens during
the rotation window (both keys valid for N days). Without a rotation policy, keys live forever.

### OAuth scopes designed as one giant `read_write` scope.

**Fix:** Scopes should map to capabilities a consumer might want without granting everything.
At minimum split read from write; ideally split by resource (`read:games`, `write:standings`).
Granular scopes let consumers ask for the minimum they need.

## Documentation

### "Just check the docs" — when the docs are hand-written and the OpenAPI spec is stale.

**Fix:** OpenAPI spec is the source of truth. Hand-written docs are generated from it (Scalar,
Stoplight, Redoc) so they can't drift. CI fails the build if the spec is invalid or doesn't
match the handler.

### Docs without runnable examples.

**Fix:** Every endpoint in the docs has a working example (curl, language SDK) that hits
staging. Examples that don't execute become wrong silently; examples that execute either work
or fail loudly.

## Freshness + provenance

### Freshness fabrication — `meta.fetched_at` set to the current request time.

**Fix:** `fetched_at` is the freshness of the underlying data, not the request handler's
clock. If the data was cached at 12:00 and the handler returns it at 12:05, `fetched_at` is
12:00. Otherwise consumers can't tell stale data from fresh.

### Hardcoded "live" or "current" labels in API response strings.

**Fix:** No `"status": "Live"` strings in API copy. Freshness is a fact computed from
metadata; the consumer renders it. Hardcoded "live" labels become lies the moment the upstream
goes down.

## How to push back

State the anti-pattern, name the specific evidence (the endpoint, the spec section, the
header), propose the minimal change, link the RFC or spec section that justifies it. One
issue at a time, confirm, move to the next.
