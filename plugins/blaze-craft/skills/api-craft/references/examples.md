# api-craft — Examples

Concrete invocations and a before/after pattern.

## Slash command invocations

```
/api-design POST /v1/scoreboard/subscriptions
```

```
/api-versioning bsi-public-api
```

```
/api-errors bsi-savant
```

```
/api-webhook game-state-changed
```

## Before / after — vague API request

**Before:** A vague request that hides the real work.

> "Add a webhook for when a game ends."

**After:** The skill rewrites the request as a measurable, contract-correct task.

> "Define a `game.completed` webhook event. Payload schema: `{ event: 'game.completed',
> game_id, sport, final_score, completed_at, version: 1 }` — versioned in the payload so
> future schema changes don't break consumers. Signed with HMAC-SHA256 over `timestamp +
> raw_body`, headers `X-BSI-Signature: t=<ts>,v1=<hex>` and `X-BSI-Event: game.completed`.
> Retry policy: 8 attempts, exponential backoff `1s,2s,4s,8s,16s,32s,64s,128s` ±25% jitter.
> No ordering guarantee — consumer reconciles via `completed_at`. Dead-letter after 8 attempts
> to a queue the consumer can replay from. Replay protection via 5-minute timestamp tolerance
> on the verifier side. Document in OpenAPI under `webhooks` (3.1 supports this natively).
> Verify with a test endpoint that signs a known payload, captures the request, and confirms
> signature verifies. Do not ship until the consumer-side verifier is documented with a working
> example in at least one language."

## Before / after — error envelope cleanup

**Before:** A request that surfaces accumulated debt.

> "The API returns errors in three different shapes. Pick one and standardize."

**After:** The skill rewrites it as a contract change with a migration plan.

> "Adopt RFC 9457 problem+json as the canonical error envelope. Schema:
> `{ type: <uri>, title, status, detail, code, instance }`. Controlled vocabulary for `code`:
> `auth_required`, `auth_invalid`, `validation_failed`, `not_found`, `rate_limited`,
> `upstream_unavailable`, `internal_error`. Map every existing error to one of these.
> Migration: ship the new envelope alongside the old for 90 days, return both
> (`Content-Type: application/problem+json` for the new, legacy shape via `Accept: ...`
> negotiation). At day 90 the old shape returns 410 Gone with a problem+json pointing to the
> migration doc. Update OpenAPI components/schemas with `Problem` and reference it from every
> error response. Lint must reject any error response that doesn't reference `Problem`."

## Before / after — pagination request

**Before:** Vague pagination ask.

> "Add pagination to the standings endpoint."

**After:** Designed against the actual data shape.

> "Standings are largely static within a season but can change mid-week. Use cursor pagination
> with the cursor encoding `(conference, win_pct_desc, team_id)` so a stable order survives
> mid-page mutations. Page-size: 25 default, 100 max. `Link: <next-url>; rel=\"next\"` (RFC
> 8288), no `total_count` in the default response (add `?include=total_count` for consumers
> who need it). Walk verification: first page returns 25, follow `next` link, get next 25,
> reach end, get empty `data` with no `next` link. Don't ship a base64-encoded offset disguised
> as a cursor — pick a real one now and the consumers don't have to migrate later."

## Before / after — versioning bump

**Before:** Premature major bump.

> "Let's bump to v2 because we want to clean things up."

**After:** Push back on the version bump itself.

> "What's the actual breaking change forcing a major version? If it's purely additive (new
> fields, new endpoints, optional new headers), v1 absorbs it. If it's a semantic change to
> existing behavior, name it specifically — that's the entry in the migration guide. If 'we
> want to clean things up' has no breaking change behind it, bump nothing; deprecate the old
> shape inside v1 with `Deprecation: true` and `Sunset` headers, and deliver the cleanup as
> additive endpoints. v2 is the option of last resort because every consumer has to migrate."

## Skill chaining

This skill works well chained with:

- `fullstack-engineer` — once the contract is locked, hand off implementation.
- `cloudflare` — for Workers / Hono handler implementation specifically.
- `supabase` — for the data layer the API speaks to.
- `auth0` — for OAuth provider configuration.
- `frontend-craft` — for client-side consumption of the contract.
- `mobile-craft` — for mobile-side consumption with offline / retry concerns.
