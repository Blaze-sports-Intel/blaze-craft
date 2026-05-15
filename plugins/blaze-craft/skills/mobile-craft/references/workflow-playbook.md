# mobile-craft — Workflow Playbook

Long-form companion to `SKILL.md`. Three core decision trees: stack-choice, cross-runtime
contract, cross-store shipping.

## Phase 1 — Intake (5 minutes)

Identify which decision tree applies:

1. "Should I build this native, RN+Expo, or Flutter?" → **stack-choice**
2. "How should this behave consistently across runtimes?" → **cross-runtime contract**
3. "How do iOS and Android stay in sync at the listing/store level?" → **cross-store
   shipping**

If the user request is actually about implementation (writing Swift, building an Xcode
workflow, configuring EAS Build), it's not a mobile-craft job — hand off to `ios-craft`,
`react-native-foundations`, or `expo`.

## Phase 2 — Source crawl

For non-trivial decisions:

1. `references/official-sources.md` is the entry point.
2. **Stack-choice questions** — Apple HIG, Material Design 3, React Native architecture
   docs, Expo docs, Flutter docs, comparative analyses from canonical engineering blogs (only
   if dated and named).
3. **Cross-runtime contract questions** — Apple's framework documentation for the iOS
   contract, Android equivalents, RN/Expo/Flutter docs for how each runtime exposes the
   capability.
4. **Cross-store shipping questions** — App Store Connect docs (App Privacy, screenshot
   specs, age ratings), Play Console docs (Data Safety, screenshot specs, content rating).

## Phase 3 — Stack-choice decision tree

When the user is choosing between native / RN+Expo / Flutter:

### Step 1 — Native-feature reach

Does the feature set require any of these?

- StoreKit 2 (subscriptions, in-app purchases with the latest server-side validation)
- App Intents / Shortcuts / Spotlight
- Live Activities, Dynamic Island, Lock Screen widgets
- ARKit / RealityKit / vision-based AR
- Vision framework (image analysis on-device)
- Apple Pay, Wallet
- HealthKit, HomeKit, CarPlay
- WidgetKit (rich widgets, not stub widgets)
- Mac Catalyst or native macOS shell
- visionOS, watchOS, tvOS

If yes — **strong pull toward native**. RN bridges exist for some of these but lag the OS
release cycle and break on major iOS updates. Flutter is even further behind on Apple-side
integration.

### Step 2 — Team capability depth

- Does the team have someone who's written production Swift?
- Does the team have someone who's shipped to TestFlight?
- Does the team have someone who's written production Kotlin?
- Does the team have RN production experience including native module bridging?

If native experience exists → native is the safer path.
If only web/JS experience → RN+Expo gets you to a shipped app fastest.
If nobody has shipped mobile at all → start with Expo (managed workflow) and learn the
shipping path before taking on native concerns.

### Step 3 — Shipping cadence

- How often will the app ship?
- Does the team need OTA updates (push code without an app review)?

If OTA matters and the feature set fits → Expo (EAS Update) is uniquely strong here.
Native iOS requires App Store review for every binary change. Flutter has community OTA
solutions but they're not first-party.

### Step 4 — Single platform vs both

- Is this iOS-only (today and likely forever)?
- Is this Android-only?
- Is this both from day one?
- Is this iOS-first with Android as a fast-follow?

If iOS-only — native iOS wins on every axis except OTA.
If Android-only — native Android (Kotlin + Compose).
If both day one and the feature set is largely UI — RN+Expo or Flutter both shine.
If iOS-first with Android fast-follow — native iOS first, and the Android decision is a
separate stack-choice when you actually start Android.

### Step 5 — The decision document

Write it down:

```
Stack: <chosen runtime>
Justified by: <constraints from steps 1-4>
Re-evaluation triggers:
  - <condition that would change the decision>
  - <condition that would change the decision>
  - <condition that would change the decision>
Implementation specialist: <ios-craft / react-native-foundations / expo>
Handoff: <what the implementing specialist needs to know>
```

## Phase 4 — Cross-runtime contract decision tree

When the question is "how should X behave consistently across runtimes":

### Pattern: offline-first sync

- **Source of truth** — local store (SQLite / SwiftData / Realm / WatermelonDB) is the
  canonical data; server is eventual.
- **Write path** — local write succeeds immediately; queue for server sync.
- **Conflict policy** — last-write-wins, three-way merge, or CRDT (rare). Document the
  choice; failure to document means whoever implements first picks one and locks the
  contract.
- **Retry policy** — exponential backoff with jitter; cap at N attempts; surface to user
  after cap.
- **Sync triggers** — on app foreground, on connectivity restored, on explicit user pull.
- **iOS implementation** → ios-craft (SwiftData, BackgroundTasks).
- **RN/Expo implementation** → react-native-foundations / expo (WatermelonDB, expo-sqlite).
- **Flutter implementation** → drift, isar.

### Pattern: push notifications

- **Routing matrix** — per notification type: trigger, audience, payload, deep link, cold
  launch behavior, background behavior, expiration.
- **APNs payload** — schema for iOS (Apple).
- **FCM payload** — schema for Android.
- **Cross-runtime parity** — the deep link target should be identical regardless of which
  platform receives it.
- **iOS implementation** → ios-craft (UNUserNotificationCenter, APNs token refresh).
- **Android implementation** → not currently on shelf; FCM token refresh + Compose deep
  link receivers when added.

### Pattern: deep linking

- **Universal Links** (iOS) — `apple-app-site-association` at
  `/.well-known/apple-app-site-association` with the `applinks` block.
- **App Links** (Android) — `assetlinks.json` at `/.well-known/assetlinks.json` with the
  app's package name and signing certificate fingerprint.
- **Deferred deep link** — for cold-install case where the user clicked the link before
  installing the app. Branch.io, AppsFlyer, or self-hosted via cookie/install-attribution.
- **Fallback to web** — if the app isn't installed and deferred deep link isn't set up, the
  link should land on a meaningful web page, not a 404.

### Pattern: biometrics

- **iOS** — LocalAuthentication framework. Touch ID / Face ID / Optic ID. Always have a
  passcode fallback.
- **Android** — BiometricPrompt API. Class 3 (strong) vs Class 2 (weak) biometric tier.
- **Cross-runtime** — RN: `react-native-biometrics` or `expo-local-authentication`. Flutter:
  `local_auth` package.
- **Failure modes** — biometric not available, biometric lockout, user cancellation.
  Document recovery behavior.

### Pattern: background work

- **iOS** — BGAppRefreshTask (short, frequent), BGProcessingTask (long, occasional). System
  decides when; you can request a window.
- **Android** — WorkManager (recommended); JobScheduler (older). Stricter doze-mode limits.
- **Cross-runtime** — RN/Expo: `expo-background-fetch`, `expo-task-manager`. Flutter:
  `workmanager` package.

## Phase 5 — Cross-store shipping decision tree

When iOS and Android both ship:

### The parity matrix

| Element | App Store Connect | Play Console | Required parity |
|---|---|---|---|
| Version number | `CFBundleShortVersionString` | `versionName` | Match (or document offset) |
| Release notes | What's New | Release notes | Same framing, story, issues |
| Screenshots | Per device size | Per device size | Same content, sized per platform |
| Privacy disclosure | App Privacy details | Data Safety form | Same data classes, same uses |
| Age rating | App Store Connect rating | IARC rating | Compatible (no contradictions) |
| Subtitle / short desc | Subtitle | Short description | Same value prop |
| Long description | Description | Full description | Same content, language tweaked per platform conventions |

### Drift-prevention discipline

- Release on the same day, or document why not.
- Same release notes file used to generate both store entries (the descriptions can be
  trimmed differently per character limit, but the story is the same).
- Privacy disclosure changes go through both stores in the same change set.
- Screenshot regeneration runs against the same source images, sized per platform device
  list.

## Phase 6 — Hand back

Tell the user:

- The decision (stack-choice) or the contract (cross-runtime) or the parity status
  (cross-store).
- Who implements next (ios-craft, react-native-foundations, expo, or future-Android).
- What changes the decision (the re-evaluation triggers).

Plain English. "We're going native iOS first because Live Activities and StoreKit 2 are in
scope, and Android picks up after if user adoption hits 5K MAU." Not "stack decision: native
iOS, justified by SAM-1, SAM-3."

## Edge cases

- **User wants both platforms but team has no native experience** — Expo first, document
  the path to ejecting if a native module becomes unavoidable.
- **Existing iOS app, user wants Android added** — start the parity matrix before the
  Android implementation; that's where most of the drift starts.
- **OTA updates pushed to all users at once** — don't. Always canary first.
- **Privacy disclosure mismatch caught at submission** — fix both stores, not just the
  flagged one. Apple's reviewer will eventually catch the Android mismatch even if it's
  Play Store that flagged first.
