---
description: Design or audit the API versioning strategy and deprecation policy for a given API.
---

Use the api-craft skill to define versioning + deprecation policy for: $ARGUMENTS

Produce:

- **Versioning mechanism** — URI prefix (`/v2/`), `Accept-Version` header, or media-type
  versioning. Justified by why this fits the consumer mix.
- **Breaking-change definition** — what counts as breaking (removed field, semantic change,
  required field added, error code semantic change, narrowed enum). Document the rules
  explicitly.
- **Deprecation cycle** — what happens between "marked deprecated" and "removed". Headers:
  `Deprecation: true` and `Sunset: <RFC 9110 date>` and
  `Link: <migration-doc>; rel="deprecation"`.
- **Migration guide skeleton** — for each deprecated endpoint, the canonical replacement and
  the steps to migrate.
- **Internal classification rule** — every PR touching the API is classified additive /
  breaking in the description. CI flag if missing.

Reference RFC 8594 (Sunset header) and the IETF Deprecation HTTP Header draft.
