---
description: Coordinate parity between App Store Connect and Play Console for a release — version numbers, release notes, screenshots, privacy disclosures, age ratings.
---

Use the mobile-craft skill to coordinate cross-store shipping parity for: $ARGUMENTS

Build the parity matrix:

| Element | App Store Connect | Play Console | Required parity |
|---|---|---|---|
| Version number | `CFBundleShortVersionString` | `versionName` | Match (or document offset) |
| Release notes | What's New | Release notes | Same framing, story, issues |
| Screenshots | Per device size | Per device size | Same content, sized per platform |
| Privacy disclosure | App Privacy details | Data Safety form | Same data classes, same uses |
| Age rating | App Store Connect rating | IARC rating | Compatible |
| Subtitle / short desc | Subtitle | Short description | Same value prop |
| Long description | Description | Full description | Same content, language tweaked per platform conventions |

For each row, report current state, required state, and the action needed.

Drift-prevention discipline:

- Release on the same day, or document why not.
- One What's New file in the repo; both stores get the same content (trimmed for character
  limits per platform, story is the same).
- Privacy disclosure changes go through both stores in the same change set.
- Screenshot regeneration runs against the same source images, sized per platform device list.
- Version numbers stay in lockstep, or the offset is documented and intentional.

Hands off implementation to ios-craft (App Store Connect side) and the future Android
implementing specialist (Play Console side).
