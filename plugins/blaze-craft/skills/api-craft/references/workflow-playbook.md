# api-craft — Workflow Playbook

Long-form companion to `SKILL.md`. The contract is the artifact; the implementation is a
consequence of the contract.

## Phase 1 — Intake (5 minutes)

Ask once, then commit:

1. **Surface** — a new resource, a new endpoint on an existing resource, a new event, a
   webhook, a versioning bump, a deprecation?
2. **Consumers** — who calls this? Web UI, mobile app, third-party integration, internal
   service? The number of consumers and the trust level changes everything (an internal
   monorepo call has different invariants than a public webhook).
3. **Scale** — requests per second, payload size, latency budget. Influences pagination,
   caching headers, rate-limit design.
4. **Existing spec** — is there an OpenAPI / GraphQL schema in the repo? If yes, it's the
   source of truth; the user request is a delta against it. If no, that absence is the first
   thing to fix.
5. **Versioning posture** — is this an additive change (new optional field, new endpoint, new
   enum value) or a breaking change (removed field, semantic change to existing field, error
   shape change)?

## Phase 2 — Source crawl

For any non-trivial decision:

1. Check the relevant entries in `references/official-sources.md`:
   - **RFCs** — 9457 (problem+json), 9110 (HTTP semantics), 8594 (`Sunset` header), 6585 (429),
     8288 (Web Linking), 7234 (caching).
   - **OpenAPI 3.1** specification.
   - **JSON Schema 2020-12** specification.
   - **OAuth 2.1** draft (current best practice consolidation).
   - **AsyncAPI** for event-driven contracts.
2. Use Context7 MCP for live SDK doc lookups when the spec uses a specific generator.
3. If a community blog is the only source, label the claim **non-authoritative**.

Never write Bearer-token semantics, OAuth scope rules, or webhook signing schemes from
training memory. Always check the current spec.

## Phase 3 — Plan

Write a 5–10 line plan before touching the spec. Include:

- The contract shape (resource model, schema, service definition).
- The versioning strategy and whether this is additive or breaking.
- The error envelope contract.
- The verification (curl transcript, schema validation, linter).
- The rollback path if the contract turns out wrong (deprecate the new shape, sunset header).

## Phase 4 — Execute

Match the capability to the artifact:

- **Choose between REST, GraphQL, gRPC, and JSON-RPC for a given surface.** → Style decision
  record naming the chosen approach with the constraint that forces it (e.g. "REST chosen
  because consumers are heterogeneous and CDN cacheability matters; would re-evaluate if a
  single rich client needed deeply nested queries").
- **Design a versioning strategy.** → Versioning + deprecation policy doc with the chosen
  mechanism (URI / header / media type), the deprecation timeline, the `Sunset` header
  values, and the migration guide skeleton.
- **Define a consistent error envelope.** → RFC 9457 problem+json shape with the controlled
  vocabulary of `code` values, mapping from internal error class to wire error, and example
  payloads for each error code.
- **Design pagination.** → Pagination spec naming the algorithm (cursor for fast-changing
  collections, offset only for static), opaque cursor format, page-size limits, link headers
  (RFC 8288), `total_count` policy.
- **Design idempotency.** → Idempotency spec with `Idempotency-Key` header semantics, replay
  window, conflict behavior when the same key arrives with a different body, how the response
  is cached server-side.
- **Design rate limiting.** → Rate-limit spec with algorithm choice, per-key vs per-IP scoping,
  header contract (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`,
  `Retry-After`), 429 behavior.
- **Design a webhook contract.** → Webhook contract doc with payload schema (versioned),
  HMAC-SHA256 signature scheme over canonical body + timestamp, retry policy (max attempts,
  exponential backoff with jitter), ordering guarantee statement, dead-letter handling,
  replay protection via timestamp + nonce.
- **Decide authentication on the wire.** → Auth spec: credential type, where it's carried
  (always header, never query string), rotation policy, scope design (if OAuth).
- **Plan SDK ergonomics.** → SDK surface plan: what to expose, what shape the client error
  type takes, sync vs async, built-in retry policy with the right defaults.
- **Establish OpenAPI / AsyncAPI as source of truth.** → Spec file committed, lint config
  (Spectral) committed, docs generation pipeline configured, examples that execute against
  staging.

## Phase 5 — Verify

Walk the matrix in `quality-rubric.md`. Capture evidence:

- Linter output (Spectral or equivalent) showing zero errors.
- curl transcript showing the wire shape matches the spec.
- Schema validation output (the response validates against the OpenAPI schema).
- Error-path curl transcript showing problem+json with a `code` from the controlled
  vocabulary.
- Pagination walk: first page → next page (using cursor) → past-end empty page.
- Idempotency walk: same key + same body returns the cached response; same key + different
  body returns the conflict.
- Rate-limit headers present on every response.
- Webhook delivery test: HMAC verifies on the consumer side; retry behavior verified via
  intentionally-failed delivery.
- Docs render and the example code in the docs actually runs against staging.

Don't claim verification you didn't run. "Should work" is not verification.

## Phase 6 — Hand back

Tell the user:

- What the wire now does that it didn't before (in user terms — "consumers can now request
  paginated games", not "added cursor query param to /games").
- What's deprecated and when it sunsets (with the exact `Sunset` header value).
- What's documented (link to the rendered OpenAPI page).
- What the consumer needs to do to migrate, if anything.

No `200`, no `400`, no status codes in the user-facing summary. Plain English.

## Edge cases

- **Existing spec doesn't match implementation** — name the divergence; ask which is canonical
  before changing either.
- **Breaking change requested without major version bump** — push back. Either it's actually
  additive (and we can find a compatible shape) or it needs a major bump.
- **Webhook ordering required but the underlying transport is HTTP** — there's no ordering
  guarantee at the protocol layer. Either add a sequence number to the payload, or use a
  different transport.
- **Idempotency without a key strategy** — clients won't deduplicate without a key shape they
  can trust. Define the key format (UUID, hash of canonical request, etc.) before the feature
  ships.
- **Deprecation without a sunset date** — stays deprecated forever, never gets removed,
  consumers ignore the warning. Always commit a `Sunset` value.
