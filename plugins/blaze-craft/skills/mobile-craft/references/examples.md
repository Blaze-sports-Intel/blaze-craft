# mobile-craft — Examples

Concrete invocations and a before/after pattern.

## Slash command invocations

```
/mobile-stack saved-items-feature
```

```
/mobile-stack new-mobile-app-from-scratch
```

```
/cross-store-ship 1.4.0
```

```
/push-matrix game-final-alerts
```

## Before / after — vague mobile request

**Before:** A vague request that hides the real work.

> "Should I build the new feature in Expo or native?"

**After:** The skill rewrites the request as a stack-choice run.

> "Run the stack-choice decision tree on this feature. Native-feature reach: does it need
> StoreKit 2, App Intents, Live Activities, ARKit, complex camera, HealthKit, Mac Catalyst?
> Team capability: who on the team has shipped Swift to TestFlight, and who has shipped RN
> with native module bridging? Shipping cadence: do we need OTA updates without going
> through App Store review? Single platform or both? Output: a stack decision record naming
> the chosen runtime, the constraints justifying it, the re-evaluation triggers, and the
> handoff to the implementing specialist (ios-craft / react-native-foundations / expo)."

## Before / after — cross-runtime push design

**Before:** Single-platform push design.

> "Wire up push notifications for the iOS app — when a game ends, ping the user."

**After:** Designed as a cross-runtime contract from the start, even if only iOS ships
today.

> "Push notification matrix for game-final alerts. Per type: trigger (game state changes to
> completed), audience (users with notification preference enabled for the game's team),
> APNs payload (`{ aps: { alert: ..., sound, category }, custom: { game_id, deep_link } }`),
> FCM payload (`{ notification: ..., data: { game_id, deep_link } }`), deep link target
> (the game detail screen with `?source=push&game=<id>`), expiration (`apns-expiration`
> header at game-start-time + 6 hours), cold launch behavior (route directly to game
> detail, no home screen interstitial), background behavior (in-app banner, route on tap).
> Hand off iOS implementation to ios-craft (UNUserNotificationCenter + APNs token refresh
> handler). Hand off Android implementation to future-Android (FCM + Compose deep link
> receiver) — design now so the contract is written when Android lands."

## Before / after — cross-store parity check

**Before:** Drift caught in submission.

> "App Store rejected our submission — they say our privacy disclosure doesn't match Play
> Store's."

**After:** Parity matrix as the response.

> "Pull the App Privacy details from App Store Connect and the Data Safety form from Play
> Console side by side. Build the parity matrix. For every data class (analytics, crash
> diagnostics, device identifiers, contact info, location): does App Store Connect say
> 'collected'? does Play Console say 'collected'? does the actual app code collect this?
> Reconcile to ground truth — what the code actually does — then update both forms to match.
> Going forward: any change to data collection requires both forms updated in the same
> change set; CI flag if the source-of-truth privacy doc is updated but either form isn't."

## Before / after — drift between stores

**Before:** Reactive after three cycles of drift.

> "iOS is at 1.4, Android is still at 1.1 because we keep deprioritizing the Android
> release."

**After:** Drift-prevention discipline as the response.

> "Two-step plan: first, get Android to feature parity with iOS 1.4 in one sprint (Android
> 1.4.0 with the same release notes). Second, lock release-train cadence: iOS and Android
> ship the same week, version numbers in lockstep. CI flag if iOS tags a release and
> Android doesn't have a corresponding release branch within N days. Privacy and screenshot
> updates go through the same change set so neither store falls behind on those either.
> The reason this matters: consumers in mixed-device households (one iPhone user + one
> Android user in a family) notice the gap, and the App Store and Play Store reviewers
> increasingly cross-check Apple Privacy Labels against Play Data Safety."

## Before / after — biometric prompt without fallback

**Before:** Mandatory biometric design.

> "Sign-in flow uses Face ID — if Face ID fails, the user can't get in."

**After:** Cross-runtime biometric contract with mandatory fallback.

> "Biometric prompt is the primary path; device passcode is the fallback. Failure modes:
> (a) biometric not available → fall back to passcode (no surprise screen); (b) biometric
> hardware lockout after 5 failed attempts → fall back to passcode; (c) user opts out of
> biometric → never prompt, always passcode; (d) biometric not enrolled → never prompt.
> iOS implementation: LAContext with `.deviceOwnerAuthentication` (allows passcode fallback
> automatically) — hand off to ios-craft. Android implementation: BiometricPrompt with
> `setAllowedAuthenticators(BIOMETRIC_STRONG | DEVICE_CREDENTIAL)` — hand off when Android
> ships. Cross-runtime contract: biometric is convenience, passcode is the security floor.
> The contract holds even if Face ID changes its tier classification in a future iOS
> update."

## Skill chaining

This skill works well chained with:

- `ios-craft` — for Apple-platform implementation of the contract.
- `react-native-foundations` — for RN implementation.
- `expo` — for Expo / EAS implementation.
- `api-craft` — for the wire contract the mobile app speaks against.
- `frontend-craft` — for shared design language between mobile and web.
