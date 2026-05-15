# Official Sources for api-craft

Ground every non-obvious technical claim in these sources. Community sources (blogs, Stack
Overflow, Reddit) are non-authoritative and may be used only as implementation inspiration.

## RFCs (always check first for HTTP semantics)

- [RFC 9457 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457) —
  current spec for problem+json. Supersedes RFC 7807.
- [RFC 7807 — Problem Details for HTTP APIs (legacy)](https://www.rfc-editor.org/rfc/rfc7807) —
  the predecessor; reference for legacy implementations.
- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — current HTTP
  semantics consolidation. Status codes, methods, header conventions.
- [RFC 9111 — HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111) — `Cache-Control`,
  `ETag`, conditional requests.
- [RFC 8594 — The Sunset HTTP Header Field](https://www.rfc-editor.org/rfc/rfc8594) —
  deprecation signaling.
- [RFC 6585 — Additional HTTP Status Codes](https://www.rfc-editor.org/rfc/rfc6585) — 428,
  429, 431, 511. The `Retry-After` semantics for 429.
- [RFC 8288 — Web Linking](https://www.rfc-editor.org/rfc/rfc8288) — `Link` header
  conventions for pagination, deprecation, etc.
- [RFC 7234 — HTTP Caching (legacy)](https://www.rfc-editor.org/rfc/rfc7234) — predecessor of
  RFC 9111.
- [RFC 7233 — Range Requests](https://www.rfc-editor.org/rfc/rfc7233) — when partial
  responses are needed.
- [RFC 6750 — Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750) — OAuth Bearer
  semantics.
- [Deprecation HTTP Header (draft)](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-deprecation-header) —
  the `Deprecation` header companion to `Sunset`.

## Specifications

- [OpenAPI 3.1 Specification](https://spec.openapis.org/oas/v3.1.0) — current OpenAPI spec.
  Includes the `webhooks` field for documenting webhook contracts natively.
- [OpenAPI 3.0 Specification](https://spec.openapis.org/oas/v3.0.3) — predecessor; still
  widely deployed.
- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/release-notes) — current JSON
  Schema spec used by OpenAPI 3.1.
- [GraphQL Specification](https://spec.graphql.org/) — canonical GraphQL spec.
- [AsyncAPI Specification](https://www.asyncapi.com/docs/reference/specification/latest) —
  for event-driven contracts (webhooks, message queues, streams).
- [OAuth 2.1 Authorization Framework (draft)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1) —
  current best-practice consolidation of OAuth 2.0.
- [OAuth 2.0 Authorization Framework (RFC 6749)](https://www.rfc-editor.org/rfc/rfc6749) —
  the base spec.
- [PKCE (RFC 7636)](https://www.rfc-editor.org/rfc/rfc7636) — required for public clients in
  modern OAuth.
- [JSON Web Token (RFC 7519)](https://www.rfc-editor.org/rfc/rfc7519) — JWT structure and
  claims.

## Style guides + best practices

- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md) —
  one of the most rigorous public REST style guides.
- [Google API Improvement Proposals (AIPs)](https://google.aip.dev/) — Google's API design
  improvement proposals; treat as a curated catalog of accumulated wisdom.
- [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/) —
  another rigorous public guide; strong on problem+json adoption.
- [Stripe API Reference](https://docs.stripe.com/api) — example of a production-grade API
  with strong versioning, idempotency, and pagination patterns.
- [GitHub REST API documentation](https://docs.github.com/rest) — canonical example of
  cursor pagination, rate-limit header conventions, conditional requests.

## Tooling

- [Spectral OpenAPI linter](https://meta.stoplight.io/docs/spectral) — most widely used
  OpenAPI linter; rules customizable.
- [Scalar API Reference](https://scalar.com) — modern OpenAPI docs renderer.
- [Stoplight Elements](https://stoplight.io/open-source/elements) — embeddable OpenAPI docs.
- [Redoc](https://github.com/Redocly/redoc) — OpenAPI docs generator.
- [Pact contract testing](https://docs.pact.io) — consumer-driven contract testing for
  service boundaries.

## Webhook signing references

- [Stripe webhook signing](https://docs.stripe.com/webhooks/signatures) — canonical example
  of HMAC-over-timestamp scheme.
- [GitHub webhook signing](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries) —
  alternative example using HMAC-SHA256.

## Source hierarchy

1. RFCs (current versions).
2. OpenAPI / JSON Schema / GraphQL / AsyncAPI specifications.
3. OAuth 2.1 draft and OAuth 2.0 RFCs.
4. Microsoft / Google / Zalando style guides.
5. Production-grade public APIs (Stripe, GitHub) for pattern examples.
6. Community examples — labeled non-authoritative.

If official docs conflict with anything in this skill, follow the official docs and update
this file with the change. Open a PR with a one-line note in the changelog.
