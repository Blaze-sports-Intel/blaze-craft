# mobile-craft — Quality Rubric

Use this rubric on PR review of any mobile-orchestration decision or before claiming any
work done. mobile-craft doesn't claim "the app is shipped" — that belongs to the
implementing specialist (ios-craft / react-native-foundations / expo). mobile-craft claims
"the decision is locked, the contract is written, the handoff is clean."

## Stack-choice verification matrix

| # | Check | Result |
|---|-------|--------|
| 1 | The decision document names the chosen runtime, the constraints, and the re-evaluation triggers. | pass / fail |
| 2 | Native-feature reach analysis is in the document (which features need native, which don't). | pass / fail |
| 3 | Team capability depth analysis is in the document (who's shipped what). | pass / fail |
| 4 | OTA-update need is explicit (yes/no with reasoning). | pass / fail |
| 5 | Single-platform vs both-platforms is explicit. | pass / fail |
| 6 | The implementing specialist (ios-craft / react-native-foundations / expo) is named. | pass / fail |
| 7 | Handoff content (what the implementing specialist needs to know) is written. | pass / fail |

## Cross-runtime contract verification matrix

| # | Check | Result |
|---|-------|--------|
| 1 | The pattern (offline sync / push / deep link / biometric / background) is named. | pass / fail |
| 2 | The runtime-agnostic contract is documented (behavior, not implementation). | pass / fail |
| 3 | Per-runtime implementation hooks are listed (iOS: X; RN: Y; Flutter: Z). | pass / fail |
| 4 | Failure modes (offline, push receipt failure, deep link miss) have documented recovery. | pass / fail |
| 5 | iOS implementation tested on a real device against the contract. | pass / fail / n/a |
| 6 | RN/Flutter implementation tested on a real device (if in play). | pass / fail / n/a |
| 7 | Push notifications: APNs payload + FCM payload both documented. | pass / fail / n/a |
| 8 | Deep links: Universal Links + App Links both configured (if both platforms ship). | pass / fail / n/a |
| 9 | Biometrics: passcode fallback documented for every biometric prompt. | pass / fail / n/a |

## Cross-store shipping verification matrix

| # | Check | Result |
|---|-------|--------|
| 1 | Parity matrix exists and shows zero drift. | pass / fail |
| 2 | Version numbers consistent (or offset documented). | pass / fail |
| 3 | Release notes framing matched between App Store Connect and Play Console. | pass / fail |
| 4 | Screenshots generated at the right sizes for both platforms from the same sources. | pass / fail |
| 5 | App Privacy details (iOS) and Data Safety form (Android) match data collection reality. | pass / fail |
| 6 | Age ratings compatible (no contradictions). | pass / fail |
| 7 | Both stores' pre-launch reports / readiness checks pass. | pass / fail |

## Definition of done

The decision is documented, the contract is written, the implementing specialist has what
they need. mobile-craft hands off clean and the next session can pick up without
re-deciding.

For stack-choice work — done means a future session can read the decision doc, understand
the chosen runtime and the constraints, and know what would force a re-evaluation. Without
having to ask the team "why did we pick this."

For cross-runtime contract work — done means iOS implementation matches the contract on a
real device, and any other runtime in play does too. The contract isn't validated by
existing — it's validated by behavior on hardware.

For cross-store shipping work — done means the parity matrix shows zero drift on the
elements that matter (version, release notes, screenshots, privacy, age rating) and both
stores' readiness checks pass.

Plus the cross-cutting baseline:

- Verification actually happened — evidence captured (decision document, contract test
  output, parity matrix screenshot).
- Handoff acknowledged in the implementing specialist's session.

## Failure modes that block "done"

- Stack-choice doc exists but doesn't name re-evaluation triggers (the decision is locked
  with no exit condition).
- Cross-runtime contract documented but never tested on a real device.
- Push notification matrix designed for iOS only when Android is also in scope.
- Deep links work on iOS, fall back to web on Android.
- Privacy disclosure mismatch between App Store Connect and Play Console.
- Implementing specialist (ios-craft / react-native-foundations / expo) wasn't told what
  the contract was, has to re-derive.
