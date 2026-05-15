# blaze-craft

Two-skill engineering pack for Claude Code. Sits *above* implementation specialists and owns
the upstream decisions and contracts that determine how the implementation gets done.

## What's in the pack

### `api-craft` — wire contract design

API design as a craft separate from API implementation. Owns the **wire contract** — the
shape of the conversation between the service and its consumers — independent of how the
service is implemented underneath.

- REST / GraphQL / gRPC / RPC choice with the constraints that justify it
- Versioning strategy (URI / header / media-type) and deprecation policy with `Sunset` headers
- Error envelope (RFC 9457 problem+json) with controlled `code` vocabulary
- Pagination patterns (cursor for fast-changing collections, offset only for static)
- Idempotency-Key semantics with same-key-different-body 409 discipline
- Rate-limit headers (`X-RateLimit-*`, `Retry-After`) and 429 behavior
- Webhook contracts with HMAC-SHA256 signing, exponential backoff + jitter, dead-letter,
  replay protection
- Authentication on the wire (Bearer / API key in header — never query string), OAuth scope
  design, rotation policy
- SDK ergonomics and OpenAPI as the documentation source of truth

Hands off implementation to `fullstack-engineer`, `cloudflare`, or whatever runtime owns the
handler.

### `mobile-craft` — mobile orchestration and decision-making

The layer above platform implementation specialists. Owns three things:

1. **Stack-choice phase** — native iOS vs RN+Expo vs Flutter, with the constraints
   documented (native-feature reach, team capability depth, shipping cadence, OTA needs,
   platforms-at-launch).
2. **Cross-runtime patterns** — offline-first sync, push delivery, deep linking, biometrics,
   background work — where iOS / RN / Expo have different shapes but the contract should
   stay consistent.
3. **Cross-store shipping discipline** — when an app eventually ships on both Apple and
   Android stores, the parity work between App Store Connect and Play Console (release
   notes, screenshots, privacy disclosures, age ratings).

Hands off Apple-platform implementation to `ios-craft`, React Native to
`react-native-foundations`, Expo to `expo`.

## Cross-cutting agents

- **api-contract-reviewer** — reviews PRs touching API surface area for breaking changes,
  error envelope consistency, versioning discipline, pagination shape, idempotency,
  rate-limit headers, webhook signing.
- **mobile-stack-decider** — walks the stack-choice decision tree and produces a stack
  decision record naming the chosen runtime, the constraints, the re-evaluation triggers,
  and the implementing specialist.

## Slash commands

- `/api-design <surface>` — full contract design pass
- `/api-versioning <api>` — versioning + deprecation policy
- `/api-errors <api>` — error envelope audit and migration to RFC 9457
- `/api-webhook <event>` — webhook contract design
- `/mobile-stack <feature>` — walk the stack-choice decision tree
- `/cross-store-ship <version>` — coordinate App Store Connect / Play Console parity
- `/push-matrix <feature>` — design push notification + deep link strategy

## Install

```bash
claude plugin marketplace add Blaze-sports-Intel/blaze-craft
claude plugin install blaze-craft@blaze-craft-marketplace
```

Restart Claude Code so the slash commands load into your active session. Verify with:

```bash
claude plugin list
claude plugin details blaze-craft
```

## What this pack is not

- Not an implementation skill. Doesn't write Swift, Kotlin, JS, Dart, or handler code.
- Not a replacement for `ios-craft`, `react-native-foundations`, `expo`, `fullstack-engineer`,
  or `cloudflare`. Composes with them.
- Not a 17-discipline meta-router. It owns two specific layers and hands everything else off.

## License

MIT. See [LICENSE](LICENSE).

## Author

Austin Humphrey · [Blaze Sports Intel](https://github.com/Blaze-sports-Intel)
