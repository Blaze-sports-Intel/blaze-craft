# Changelog

All notable changes to blaze-craft are documented here.

## [1.0.0] - 2026-05-15

### Added — initial release

Two-skill engineering pack: `api-craft` (wire contract design) + `mobile-craft` (mobile
orchestration and decision-making). Both skills sit *above* implementation specialists and
hand off to them.

#### `api-craft` skill

- Owns wire contract design: REST / GraphQL / gRPC / RPC choice, versioning strategy,
  breaking-change discipline, error envelope (RFC 9457 problem+json), pagination, idempotency,
  rate limiting, webhook contracts (HMAC signing, retry policy, dead-letter, replay
  protection), authentication on the wire, SDK ergonomics, OpenAPI as source-of-truth.
- Hands off implementation to `fullstack-engineer`, `cloudflare`, or other runtime
  specialists.
- Five reference packs: workflow-playbook, anti-patterns (BSI-flavored — meta envelope,
  freshness fabrication, status codes in user copy), quality-rubric (20 verification
  rows), examples, official-sources (RFCs, OpenAPI 3.1, JSON Schema, OAuth 2.1, AsyncAPI).

#### `mobile-craft` skill

- Owns mobile decision and orchestration: stack-choice phase (native vs RN+Expo vs Flutter),
  cross-runtime patterns (offline-first sync, push delivery, deep linking, biometrics,
  background work), cross-store shipping discipline (App Store Connect / Play Console
  parity).
- Hands off Apple-platform implementation to `ios-craft`, React Native to
  `react-native-foundations`, Expo to `expo`.
- Android carried as sub-domain reference; not the centerpiece since BSI hasn't shipped
  Android yet.
- Five reference packs with the same structure as api-craft.

#### Cross-cutting agents

- `api-contract-reviewer` — reviews PRs touching API surface for breaking changes, error
  envelope consistency, versioning, pagination, idempotency, rate-limit headers, webhook
  signing.
- `mobile-stack-decider` — walks the stack-choice decision tree and produces a stack
  decision record.

#### Slash commands (7)

- `/api-design <surface>` — full contract design pass
- `/api-versioning <api>` — versioning + deprecation policy
- `/api-errors <api>` — error envelope audit and migration to RFC 9457
- `/api-webhook <event>` — webhook contract design
- `/mobile-stack <feature>` — walk the stack-choice decision tree
- `/cross-store-ship <version>` — coordinate App Store Connect / Play Console parity
- `/push-matrix <feature>` — design push notification + deep link strategy

#### Validation

- Shared `scripts/validate_skill.py` with thin per-skill wrappers (no per-skill validator
  duplication).
- `scripts/validate_all.py` walks `skills/` and runs the shared validator against each.
- GitHub Actions workflow runs validators on every push and PR.

### What this pack replaces

Lessons from `uber-engineer` (uninstalled 2026-05-15):

- 17 generic discipline skills that wrapped existing deeper specialists added no value.
- The two real gaps were API design (no specialist on the shelf) and mobile orchestration
  (the layer above ios-craft / react-native-foundations / expo).
- Two focused skills with clean "owns this, not that" lines vs the existing specialists,
  not a 17-discipline meta-router.
