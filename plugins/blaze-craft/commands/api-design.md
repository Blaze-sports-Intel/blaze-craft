---
description: Run a full api-craft contract design pass on a new or changed surface. Produces the contract shape, OpenAPI / GraphQL spec entries, error envelope, pagination + idempotency + rate-limit specs as applicable.
---

Use the api-craft skill to design the wire contract for: $ARGUMENTS

Walk the workflow:

1. **Intake** — what surface is being designed, who consumes it, scale expectations.
2. **Inspect** — read the existing OpenAPI / GraphQL spec; if absent, that's finding #1.
3. **Source-check** — RFC 9457 (problem+json), OpenAPI 3.1, RFC 9110 (HTTP semantics), RFC
   8288 (Web Linking), RFC 6585 (429), RFC 8594 (Sunset).
4. **Plan** — contract shape, versioning posture, error envelope, verification path,
   rollback.
5. **Execute** — produce the contract document and the spec entries.
6. **Verify** — spec validates, error envelope is problem+json with controlled `code`
   vocabulary, pagination/idempotency/rate-limit headers documented as applicable, webhook
   contract signed if applicable.
7. **Hand back** — what the wire now does, what's deprecated and when it sunsets.

Hands off to fullstack-engineer / cloudflare for handler implementation.
