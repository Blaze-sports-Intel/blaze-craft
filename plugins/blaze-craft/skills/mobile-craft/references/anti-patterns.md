# mobile-craft — Anti-Patterns

Push back when you see these. Each ships with a concrete fix path.

## Stack-choice anti-patterns

### Stack chosen before knowing the team's actual native depth.

**Fix:** Run the stack-choice decision tree (workflow-playbook Phase 3) before the choice is
made. Native-feature reach + team capability depth + shipping cadence + platforms-at-launch
all factor in. "We picked RN because the JS dev had bandwidth" is not a stack-choice; it's a
team-capacity decision dressed up as one.

### "Cross-platform" chosen for a surface that demands deep native integration.

**Fix:** Inventory the native features the surface needs (StoreKit 2, App Intents, Live
Activities, ARKit, complex camera, HealthKit). If three or more on the list — go native. The
RN/Flutter bridges for these features lag the OS release cycle and break on major iOS
updates. The cost of bridging poorly is higher than the cost of writing it native.

### iOS app cloned to Android by lifting the UI 1:1.

**Fix:** Android has its own conventions — predictive back, edge-to-edge, Material 3 dynamic
color, system bars, navigation rail vs bottom nav. The iOS surface is a starting reference,
not a target. Each surface gets adapted, not copied.

### Choosing Expo specifically to avoid native code, then hitting a native-required feature.

**Fix:** Decide upfront whether ejection from managed workflow is acceptable. If "no
native code ever" is a hard constraint, the feature set has to fit Expo's surface; if a
native module is plausibly needed, plan for it (someone on the team needs to be able to
write Swift and Kotlin, or budget for contracted native work).

### OTA-updates chosen as a feature without a rollback plan.

**Fix:** Every OTA update strategy needs canary cohort + rollback path documented. EAS
Update channels make this easy; CodePush has it; rolling your own without these is a footgun.
A bad OTA update has the same blast radius as a bad release but without the App Store /
Play Store review delay protecting users.

## Cross-runtime contract anti-patterns

### Push notification matrix designed only for one platform.

**Fix:** The matrix has to handle APNs and FCM both, even if Android isn't shipping yet.
The deep link target should be identical regardless of which platform delivers the
notification. Designing for iOS only and "we'll figure out Android later" means re-designing
the contract when Android lands.

### Deep links work on iOS via Universal Links but Android falls back to a web link.

**Fix:** Configure App Links the same time as Universal Links — `assetlinks.json` at
`/.well-known/assetlinks.json` with the package name and signing certificate fingerprint.
Both platforms get first-class deep link routing or neither does.

### Offline-first sync where conflict policy isn't documented.

**Fix:** Document the conflict policy explicitly. Last-write-wins, three-way merge, or CRDT.
"Whatever the implementer picks" produces different behavior on different platforms and
makes the multi-device case undebuggable. Document, then implement to the doc.

### Background sync schedules that ignore platform doze-mode realities.

**Fix:** iOS BGAppRefreshTask is best-effort; the system schedules it. Android WorkManager
respects doze mode. Don't promise "syncs every 15 minutes" — promise "best-effort sync at
least every N hours when conditions allow." Set user expectations accordingly.

### Biometric prompts without a passcode fallback.

**Fix:** Always offer device-passcode fallback when biometric fails (lockout, hardware
unavailable, user opts out). Mandatory biometric is a UX failure when biometric isn't
available — and it's a real percentage of installs.

## Cross-store shipping anti-patterns

### Cross-store releases where iOS ships first and Android drifts a release behind every cycle.

**Fix:** Ship on the same day or document why not. After three cycles of drift, the two
stores have visibly different feature sets and consumers in mixed-device households notice.
Drift-prevention discipline (workflow-playbook Phase 5) is the antidote.

### App Store Connect privacy disclosure says one thing, Play Data Safety form says another.

**Fix:** Both forms get filled out from the same source-of-truth doc. When the data
collection changes, both forms get updated in the same change set. Apple reviewers and Play
reviewers both eventually catch the inconsistency, and the rejection cycle compounds.

### Release notes framed differently for the two stores.

**Fix:** One What's New file in the repo; both stores get the same content (trimmed for
character limits per platform, but the story is the same). Different framing makes consumers
think the two apps are different products.

### Screenshots generated at iOS sizes only, Android stretched in.

**Fix:** Screenshot regeneration runs against the same source images, sized per platform
device list. Both stores get crisp screenshots; neither gets stretched stand-ins.

### Version numbers diverge silently.

**Fix:** Version numbers stay in lockstep, or the offset is documented and intentional
(e.g. "Android is exactly one version behind because we ship iOS one week ahead by
release-train policy"). Silent drift makes it impossible to talk about "version 1.4" without
asking which store.

## Observability anti-patterns

### Crash reports going to one platform's reporter only.

**Fix:** Both platforms send crashes to a single reporter (Sentry, Firebase Crashlytics,
self-hosted) so the dashboard shows both. Comparing iOS-side and Android-side crash rates
requires both being measured the same way.

### PII logged without considering the platform privacy regime.

**Fix:** OSLog Privacy annotations on iOS (`Privacy.public`, `Privacy.private`,
`Privacy.sensitive`); structured logging on Android with similar discipline. Logs persist
on-device and can be exported via crash reports — PII in logs becomes a privacy disclosure
issue.

## How to push back

State the anti-pattern, name the specific evidence (the stack-choice doc, the parity matrix,
the deep link config), propose the minimal change, link the platform doc that justifies it.
One issue at a time, confirm, move to the next.
