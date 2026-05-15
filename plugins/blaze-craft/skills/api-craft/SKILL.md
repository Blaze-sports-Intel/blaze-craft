---
name: api-craft
description: "Wire contract design — REST, GraphQL, RPC, gRPC choice, versioning strategy, breaking-change discipline, error envelope schemas, pagination patterns, idempotency keys, rate-limit semantics, webhook contracts (signing / retry / ordering), authentication on the wire, SDK ergonomics, and API documentation as the developer entry point. Use when the user mentions: API design, API contract, REST API, GraphQL, gRPC, RPC, OpenAPI, Swagger, JSON Schema, AsyncAPI, problem+json, RFC 9457, RFC 7807, error envelope, error code, pagination, cursor pagination, offset pagination, idempotency, idempotency key, rate limit, rate limiting, 429, X-RateLimit, Retry-After, webhook, webhook signing, HMAC, retry policy, dead-letter, exponential backoff, jitter, API versioning, semantic versioning, breaking change, deprecation, Sunset header, content negotiation, API authentication, Bearer token, API key, OAuth scopes, mTLS, SDK design, API SDK, API docs, developer experience, DX, contract testing, Pact, Spectral, OpenAPI lint. Pair with fullstack-engineer / cloudflare for handler implementation, supabase for data layer, auth0 for auth provider config. Do NOT trigger for: handler implementation (use fullstack-engineer / cloudflare); database schema design (use supabase); auth provider configuration (use auth0 / supabase); UI work consuming an API (use frontend-craft)."
---

# api-craft

API design as a craft separate from API implementation. This skill owns the **wire contract** —
the shape of the conversation between the service and its consumers — independent of how the
service is implemented underneath.

## When to use this skill

Triggers: API design, API contract, REST, GraphQL, gRPC, RPC, OpenAPI, Swagger, JSON Schema,
AsyncAPI, problem+json (RFC 9457 / RFC 7807), error envelope, error code, pagination (cursor or
offset), idempotency, idempotency key, rate limit, 429, `X-RateLimit-*`, `Retry-After`, webhook,
HMAC signature, retry policy, dead-letter queue, exponential backoff, jitter, API versioning,
breaking change, deprecation, `Sunset` header, content negotiation, Bearer token, API key, OAuth
scopes, mTLS, SDK design, API SDK, API docs, developer experience, DX, contract testing, Pact,
Spectral, OpenAPI lint.

Use when the user wants any of:

- Choose between REST, GraphQL, gRPC, and JSON-RPC for a given surface, with the constraints
  that would force a different choice.
- Design a versioning strategy (URI prefix, `Accept-Version` header, media-type versioning) and
  the deprecation / `Sunset` policy that goes with it.
- Define an error envelope schema that's consistent across every endpoint (RFC 9457 problem+json
  by default, with machine-readable `code` discipline).
- Design pagination (cursor for fast-changing collections, offset for static, page-size limits,
  whether `total_count` is returned and at what cost).
- Design idempotency: idempotency-key header, replay window, semantics on retry, what happens
  when the same key arrives with a different body.
- Design rate limiting: token bucket vs leaky bucket semantics, `X-RateLimit-Limit` /
  `X-RateLimit-Remaining` / `X-RateLimit-Reset` / `Retry-After` headers, 429 behavior.
- Design webhook contracts: signing (HMAC-SHA256 with timestamp), retry policy with exponential
  backoff and jitter, ordering guarantees, dead-letter handling, replay protection.
- Decide authentication on the wire: Bearer token, API key in header (not query string), mTLS,
  OAuth scope design, rotation policy.
- Design the SDK surface — what to expose, what to hide, what shape the error type should take
  on the client side, async vs sync.
- Establish OpenAPI / AsyncAPI as the single source of truth and the docs as the entry point
  for every developer touching the API.
- Establish backward-compatibility discipline — what counts as a breaking change, what doesn't,
  when to bump the major.

## When NOT to use this skill

- **Handler implementation** — use `fullstack-engineer` or `cloudflare` (Workers, Hono).
- **Database schema design** — use `supabase` or the runtime's data layer skill.
- **Auth provider configuration** (Supabase Auth, Auth0, Clerk wiring) — use `supabase` /
  `auth0`.
- **Pure UI consuming an API** — use `frontend-craft`.
- **Internal RPC between services in the same monorepo** that won't ever cross a network
  boundary — that's a function call dressed up as an API; lean on type signatures instead.

## Workflow

1. **Intake.** Read the user intent. What surface is being designed (a new endpoint, a new
   resource, a new event, a webhook)? Who consumes it (web UI, mobile app, third-party
   integration)? What's the rate / scale expectation?
2. **Inspect.** Read the existing API surface. If there's an OpenAPI spec, that's the source of
   truth. If not, read the handler code and infer the contract — and flag the absence of a spec
   as the first thing to fix.
3. **Source-check.** Ground non-trivial claims in `references/official-sources.md` — RFCs
   (9457, 9110, 8594, 6585), OpenAPI 3.1 spec, JSON Schema 2020-12, OAuth 2.1 draft, AsyncAPI.
4. **Plan.** Write a 5–10 line plan: the contract shape, the versioning strategy, the error
   envelope, the verification you'll run on the wire (curl + schema validation), and the
   rollback path if the contract turns out wrong.
5. **Execute.** Match the capability to the artifact (see Phase 4 in `workflow-playbook.md`).
6. **Verify.** A real client (curl / SDK / test harness) calls the endpoint, gets the expected
   shape, schema-validates against OpenAPI, and the error path returns problem+json. See
   `quality-rubric.md` for the full matrix.
7. **Hand back.** Report what shipped on the wire, what consumers can do that they couldn't
   before, what's deprecated and when it sunsets. Plain English. The OpenAPI spec is the source
   of truth — never describe the API by hand-paraphrasing it.

## Artifacts this skill produces

- **Contract shape document** — the chosen style (REST resource model / GraphQL schema / gRPC
  service definition), with the constraint that justified the choice.
- **OpenAPI 3.1 spec or GraphQL schema** as the canonical artifact, committed alongside the
  code that implements it.
- **Versioning + deprecation policy** — how versions are exposed, deprecation timeline,
  `Sunset` header values, migration guide.
- **Error envelope spec** — RFC 9457 problem+json shape, the controlled vocabulary of `code`
  values, the mapping from internal error to wire error.
- **Pagination spec** — cursor opaque-token strategy, page-size limits, `next` / `prev` link
  headers (RFC 8288), how `total_count` is or isn't returned.
- **Idempotency spec** — `Idempotency-Key` header semantics, replay window, conflict behavior
  when the same key arrives with a different body.
- **Rate limit spec** — algorithm (token bucket vs sliding window), per-key vs per-IP, header
  contract, 429 behavior with `Retry-After`.
- **Webhook contract** — payload schema, HMAC signing scheme with timestamp, retry policy
  (count, backoff, jitter), ordering guarantee level, dead-letter handling, replay protection
  via timestamp + nonce.
- **Authentication spec** — what credentials, where they're carried (header — not query
  string), rotation policy, scope design if OAuth.
- **SDK ergonomic plan** — surface (what to expose), error type shape on the client, sync vs
  async, retry policy in the SDK itself.
- **API docs entry point** — OpenAPI rendered (Scalar, Stoplight, Redoc), with examples that
  actually run against staging.

## Anti-patterns this skill pushes back against

The full catalog with concrete fixes lives in `references/anti-patterns.md`. Highlights:

- Endpoints returning data without a `meta` envelope (no `source`, no `fetched_at`, no
  `timezone`).
- Different error shapes per endpoint within the same API.
- Pagination via offset on tables that change frequently (causes skipped or duplicated rows).
- Webhook delivery without HMAC signatures.
- API keys carried in query strings (logged in CDN, browser history, server access logs).
- Breaking changes shipped in a minor version.
- "Just check the docs" — when the docs were hand-written and the OpenAPI spec is stale.
- 429 returned without `Retry-After` (client retries immediately, makes it worse).
- Idempotency-key replays that succeed silently when the body differs from the original.
- Status codes leaking into user-facing copy ("404 not found" shown to humans).
- Freshness fabrication — `meta.fetched_at` populated with the current request time instead of
  the upstream data's actual freshness.

## Verification required before claiming done

- The OpenAPI / GraphQL spec is committed and validates (Spectral or equivalent linter, no
  errors).
- A real client (curl or SDK) successfully calls every changed endpoint and receives the
  expected shape.
- Schema validation passes on the response.
- The error path returns problem+json with a `code` from the controlled vocabulary.
- Pagination is verified end-to-end on a real collection (request next page, get next page,
  request after end, get empty page).
- Idempotency is verified — same key + same body returns the same response; same key +
  different body returns a 409 (or the documented behavior).
- Rate-limit headers are present on every response.
- Webhook payload is signed with HMAC and the signature verifies on a real consumer.
- The docs render and the example code runs against staging.

## Suggested commands

- `/api-design <surface>` — full contract design pass on a new or changed surface.
- `/api-versioning <api>` — versioning strategy and deprecation policy.
- `/api-errors <api>` — error envelope review and controlled-vocabulary cleanup.
- `/api-webhook <event>` — webhook contract design with signing, retry, dead-letter.

## References (load on demand)

- `references/official-sources.md` — RFCs, OpenAPI 3.1, JSON Schema, OAuth 2.1, AsyncAPI.
- `references/workflow-playbook.md` — long-form workflow with Phase 4 capability→artifact map.
- `references/anti-patterns.md` — full anti-pattern catalog with concrete fixes.
- `references/quality-rubric.md` — pass/fail rubric for contract review.
- `references/examples.md` — real before/after invocations.

## Scripts

- `scripts/validate_skill.py` — sanity-checks SKILL.md frontmatter and references via the
  shared plugin-level validator.

## Definition of done

A real client calling the API gets a predictable, documented, schema-valid response — and the
error path is just as predictable as the success path. Build success on the maintainer's
machine is not done. 200 from the handler is not done. The contract-specific states below all
need to hold:

- **Spec committed** — OpenAPI 3.1 / GraphQL schema in the repo, validated by a linter, with
  the latest changes reflected.
- **Wire-verified** — a real client call against staging returns the documented shape.
- **Error path** — failure returns problem+json (RFC 9457), with a `code` from the controlled
  vocabulary, and the HTTP status matches the semantic.
- **Headers** — pagination links, rate-limit headers, idempotency echo all present where
  documented.
- **Webhook** — payload signed, retry policy documented, dead-letter handling defined.
- **Backward compatibility** — no breaking changes inside a major version; deprecations carry
  a `Sunset` header and a documented migration path.
- **Docs** — OpenAPI rendered and the examples actually execute against staging.

Verification actually happened — evidence captured (curl transcript, linter output, schema
validation result, signed webhook delivery log).
