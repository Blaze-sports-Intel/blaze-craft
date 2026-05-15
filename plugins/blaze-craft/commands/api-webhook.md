---
description: Design a webhook contract — payload schema, HMAC signing, retry policy, dead-letter, replay protection, ordering statement.
---

Use the api-craft skill to design the webhook contract for: $ARGUMENTS

Produce:

- **Payload schema (versioned)** — the event payload shape, with a `version` field so future
  schema changes don't break consumers. Documented in OpenAPI 3.1's `webhooks` field
  (natively supported).
- **Signing scheme** — HMAC-SHA256 over `timestamp + raw_body`. Headers:
  `X-Signature: t=<unix-ts>,v1=<hex>` and `X-Event-Type: <event>`. Signing secret rotation
  policy.
- **Retry policy** — max attempts (typical: 8), exponential backoff (1s, 2s, 4s, 8s, 16s,
  32s, 64s, 128s) with ±25% jitter to avoid thundering herd.
- **Dead-letter handling** — after max attempts, payload sent to a DLQ the consumer can
  replay from. Document retention.
- **Replay protection** — consumer rejects deliveries whose timestamp is older than 5
  minutes (tolerance window). Even with valid signature, captured deliveries can't be
  replayed later.
- **Ordering guarantee statement** — explicit. HTTP delivery has none inherently; either add
  a sequence number to the payload (consumer reconciles via `event_id` or `created_at`), or
  document that ordering is best-effort.
- **Consumer verifier example** — at least one language, signed-payload-in / verified-out,
  ready to copy into consumer docs.
- **Test endpoint** — a way for consumers to test signature verification before going live.

Reference Stripe and GitHub webhook signing as canonical patterns.
