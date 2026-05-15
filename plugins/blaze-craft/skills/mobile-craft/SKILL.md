---
name: mobile-craft
description: "Mobile orchestration and decision-making — the layer above platform implementation skills. Owns stack-choice phase (native vs RN+Expo vs Flutter, with constraints documented), cross-runtime patterns (offline-first sync, push delivery, deep linking, biometrics, background work where iOS / RN / Expo have different shapes but the contract should stay consistent), and cross-store shipping discipline (parity between App Store Connect and Play Console for release notes, screenshots, privacy disclosures). Hands off Apple-platform implementation to ios-craft, React Native to react-native-foundations, Expo to expo. Android is a sub-domain reference, not a primary focus, since shipping has been Apple-platform-led to date. Use when the user mentions: mobile, mobile app, native app, mobile stack, native vs Expo, native vs React Native, native vs Flutter, RN vs Expo, Expo vs native, Flutter vs RN, mobile architecture, mobile shipping, cross-platform, cross-runtime, cross-store, App Store + Play Store, App Store Connect + Play Console, parity release, mobile release plan, mobile push, deep link strategy, Universal Links, App Links, deferred deep link, offline-first, mobile offline sync, mobile background sync, mobile biometrics, Touch ID, Face ID, Android biometrics, mobile observability. Do NOT trigger for: Apple-platform implementation (use ios-craft); React Native implementation (use react-native-foundations); Expo / EAS implementation (use expo); web responsive (use frontend-craft); pure 3D scene that isn't a shipped app (use game-development or ar-vr-development)."
---

# mobile-craft

The mobile **decision and orchestration** layer. Sits above the platform implementation
specialists — ios-craft (Apple), react-native-foundations (RN), expo (Expo / EAS) — and owns
the choices that get made *before* any of them is invoked, plus the patterns that have to
hold consistent *across* whichever ones are chosen.

This is not an implementation skill. It does not write Swift, Kotlin, JS, or Dart. It writes
the decisions that determine which language ends up getting written and the contracts that
keep behavior consistent regardless of language.

## When to use this skill

Triggers: mobile, mobile app, native app, mobile stack, native vs Expo, native vs React Native,
native vs Flutter, RN vs Expo, Expo vs native, Flutter vs RN, mobile architecture, mobile
shipping, cross-platform, cross-runtime, cross-store, App Store + Play Store, App Store
Connect + Play Console, parity release, mobile release plan, mobile push, push notification
strategy, deep link strategy, Universal Links, App Links, deferred deep link, offline-first,
mobile offline sync, mobile background sync, mobile biometrics, Touch ID, Face ID, Android
biometrics, mobile observability.

Use when the user wants any of:

- **Stack-choice phase** — pick between native iOS+Android, RN+Expo, or Flutter, with the
  constraints documented (team capability depth, surface complexity, native-feature reach,
  shipping cadence, OTA update needs, single-platform-only vs both-from-day-one).
- **Cross-runtime patterns** — define a behavior contract that stays consistent regardless of
  the underlying runtime: offline-first sync, push notification routing, deep link
  destinations, biometric prompts, background sync schedules.
- **Cross-store shipping discipline** — when an app eventually ships on both Apple and
  Android stores, the parity work between App Store Connect and Play Console (release notes
  framing, screenshot sets at the right device sizes for both, privacy disclosures matched
  between Apple Privacy Labels and Play Data Safety, age rating consistency).
- **Mobile observability strategy** — what to log, what to send to MetricKit / Firebase
  Crashlytics / Sentry, how to handle PII in logs across both stores' privacy regimes.
- **Mobile release coordination** — when an iOS-only app is about to add Android, what the
  drift-prevention discipline looks like.

## When NOT to use this skill

- **Apple-platform implementation** (Swift, SwiftUI, Xcode, App Store Connect submission
  mechanics, Liquid Glass, App Intents) — use `ios-craft`.
- **React Native implementation** (RN-specific APIs, Hermes profiling, native module
  bridging) — use `react-native-foundations`.
- **Expo / EAS implementation** (EAS Build profiles, EAS Update channels, Expo Router,
  expo-image, etc.) — use `expo`.
- **Android implementation** (Kotlin, Jetpack Compose, Gradle variants, Play Console
  submission mechanics) — currently no specialist on the shelf; this skill carries Android as
  a sub-domain *reference* but doesn't go deep, since BSI hasn't shipped Android yet.
- **Web responsive** — use `frontend-craft`.
- **Pure 3D scene that isn't a shipped app** — use `game-development` or `ar-vr-development`.

## Workflow

1. **Intake.** Identify which of the three core questions is being asked:
   - "Should I build this native, RN+Expo, or Flutter?" → stack-choice
   - "How should this behave across iOS and the other runtimes?" → cross-runtime pattern
   - "How do iOS and Android stay in sync when both ship?" → cross-store shipping
2. **Inspect.** Read what's already shipped. If there's already an iOS app and the question
   is about adding Android, the answer is shaped by parity-with-existing. If both are
   greenfield, the answer is shaped by team capability and the specific feature set.
3. **Source-check.** Ground in `references/official-sources.md` — Apple HIG, Material 3,
   React Native architecture docs, Expo docs, Flutter docs, Apple Privacy Labels guidance,
   Play Data Safety guidance.
4. **Plan.** Write the decision document. For stack-choice: chosen runtime + the constraints
   that justify it + what would force a re-evaluation. For cross-runtime patterns: the
   contract + how each runtime implements it. For cross-store shipping: the parity matrix.
5. **Hand off.** This skill produces decisions and contracts; the implementation lives in
   `ios-craft` / `react-native-foundations` / `expo`. Be explicit about the handoff.
6. **Verify.** For stack-choice: the team can articulate the chosen runtime and the
   constraints. For cross-runtime: a real test on at least the iOS side proves the contract
   holds. For cross-store: the parity matrix shows no drift between the two stores' listings.
7. **Hand back.** Plain English. "We're going native iOS first because of X, Y, Z; Android
   added in the second half if Y holds." Not "I created a 47-line stack decision record."

## Apple Build Evidence Loop (orchestration view)

Even though this skill doesn't own Apple implementation, the orchestration layer needs to
know what the Apple shipping ladder looks like in order to coordinate with cross-store work.
The summary:

1. Local clean build before any RC tag.
2. Distribute Xcode Cloud workflow (not the CI-only one) tagged.
3. Archive ≠ Upload ≠ Install — three distinct steps; "live on TestFlight" only after the
   install list shows the build on a real tester.
4. App Store Connect readiness checks all green before submit.
5. Release branch merged back to main same day after archive.

ios-craft owns the depth on each of these. mobile-craft just needs to know the order so it
can sequence Android parity work alongside it.

## Artifacts this skill produces

- **Stack decision record** — chosen runtime, constraints that justify it, native-feature
  reach analysis, OTA-update need analysis, shipping cadence, what would force a
  re-evaluation.
- **Cross-runtime contract** — for each pattern (offline sync, push, deep link, biometrics,
  background work), the behavior that should hold regardless of runtime, plus the
  runtime-specific implementation hooks.
- **Push notification matrix** — per notification type: trigger, audience, payload, deep link
  destination, expiration, what happens on tap from cold launch vs background, parity
  between APNs and FCM.
- **Deep link strategy** — Universal Links (iOS) + App Links (Android) configuration,
  associated-domain hosting, deferred deep link handling for cold-install, fallback to web.
- **Offline-first sync contract** — source of truth (local SQLite / SwiftData / Realm /
  WatermelonDB), conflict resolution policy, retry budget, sync trigger conditions.
- **Cross-store parity matrix** — release notes framing matched between App Store Connect
  and Play Console; screenshot sets at the right device sizes; privacy disclosures matched
  between Apple Privacy Labels and Play Data Safety; age ratings.
- **Mobile observability plan** — what gets logged where (OSLog on iOS, structured logs on
  Android, third-party crash reporter), PII handling per platform privacy regime, dashboard
  surfaces.
- **Release coordination plan** — when a second platform is added, the drift-prevention
  discipline (release-train cadence, version numbering parity, feature gating).

## Anti-patterns this skill pushes back against

The full catalog with concrete fixes lives in `references/anti-patterns.md`. Highlights:

- Stack chosen before knowing the team's actual native depth.
- "Cross-platform" chosen for surface that demands deep native integration (StoreKit, App
  Intents, Live Activities, complex camera, ARKit / RealityKit).
- iOS app cloned to Android by lifting the UI 1:1 — ignores Material conventions, predictive
  back, edge-to-edge.
- Cross-store releases where iOS ships first and Android drifts a release behind every cycle
  until they're three versions apart.
- Push notification matrix designed only for one platform.
- Deep links work on iOS via Universal Links but Android falls back to a web link because
  App Links wasn't configured.
- Apple Privacy Labels say one thing and Play Data Safety says another for the same data
  collection.
- OTA updates pushed to production without a canary cohort or rollback path.
- Choosing Expo specifically to avoid native code, then hitting a feature that requires
  native modules, then bridging poorly because nobody on the team writes Swift or Kotlin.

## Verification required before claiming done

### Stack-choice decisions

- The decision record names the chosen runtime, the constraints, and the re-evaluation
  trigger.
- The team can articulate the choice without reading the document.
- The choice is consistent with native-feature reach analysis (if the feature set requires
  StoreKit 2, App Intents, or Live Activities, native; if not, the runtime choice is open).

### Cross-runtime patterns

- The contract is written down (not lore).
- iOS implementation tested on a real iPhone and matches the contract.
- If RN or Flutter is in play, that runtime's implementation tested on a real device and
  matches the contract.
- Failure modes (offline, push receipt failure, deep link miss) all have documented
  recovery behavior.

### Cross-store shipping

- The parity matrix shows zero drift in release notes framing, screenshot sets, and privacy
  disclosures.
- The version numbers are consistent between stores (or the offset is documented and
  intentional).
- Both stores' pre-launch reports / readiness checks pass.

## Suggested commands

- `/mobile-stack <feature>` — walk the stack-choice phase for a new feature or app.
- `/cross-store-ship <version>` — coordinate parity between App Store Connect and Play
  Console.
- `/push-matrix <feature>` — design the push notification + deep link routing strategy.

## References (load on demand)

- `references/official-sources.md` — Apple HIG, Material 3, RN, Expo, Flutter, privacy
  guidance for both stores.
- `references/workflow-playbook.md` — long-form workflow with the three core decision trees.
- `references/anti-patterns.md` — full anti-pattern catalog with concrete fixes.
- `references/quality-rubric.md` — pass/fail rubric for orchestration decisions.
- `references/examples.md` — real before/after invocations.

## Scripts

- `scripts/validate_skill.py` — sanity-checks SKILL.md frontmatter and references via the
  shared plugin-level validator.

## Definition of done

The decision is documented and the team can act on it. For stack-choice: the chosen runtime
is recorded with its justification and the implementation specialist can pick up the work.
For cross-runtime: the contract is written and the implementing skill can verify against it.
For cross-store: the parity matrix shows no drift between the two stores' listings.

This skill doesn't claim "the app is shipped" — that's `ios-craft`'s definition of done, or
`react-native-foundations`'s, or `expo`'s. This skill claims "the decision is locked, the
handoff is clean, and the implementing specialist has what they need."

Verification actually happened — evidence captured (decision document, contract document,
parity matrix screenshot, handoff acknowledgment in the implementing skill's session).
