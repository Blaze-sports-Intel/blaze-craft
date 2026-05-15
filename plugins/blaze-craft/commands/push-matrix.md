---
description: Design the push notification + deep link routing strategy for a feature, with APNs and FCM payloads + cold-launch and background behavior documented.
---

Use the mobile-craft skill to design the push notification matrix for: $ARGUMENTS

Per notification type, document:

- **Trigger** — what event fires this notification (game state change, score update,
  scheduled time, user action elsewhere).
- **Audience** — who receives it (all users, opted-in users, users with specific
  preferences, cohort).
- **APNs payload (iOS)** — `{ aps: { alert, sound, category, "thread-id" }, custom: { ... } }`.
- **FCM payload (Android)** — `{ notification: { ... }, data: { ... } }`.
- **Deep link target** — the in-app screen with query params for source attribution
  (`?source=push&type=<event>&id=<entity_id>`).
- **Expiration** — `apns-expiration` header value (timestamp after which the notification
  is irrelevant); FCM equivalent.
- **Cold launch behavior** — on tap from a cold-killed app, route directly to the deep link
  target (no home-screen interstitial that loses context).
- **Background behavior** — in-app banner, route on tap to deep link.
- **Permissions handling** — what to do if notifications aren't enabled (silent fail vs
  in-app prompt, when and how).

Cross-runtime contract:

- Deep link target identical across APNs and FCM payloads.
- Same notification semantic on both platforms — Android's notification channels match the
  iOS category groupings.
- Failure modes (delivery rejected, token expired) handled with the same recovery semantics.

Hands off iOS implementation to ios-craft (UNUserNotificationCenter + APNs token refresh).
Hands off Android implementation to the future-Android specialist (FCM + Compose deep link
receiver) — design now even if Android isn't shipping yet, so the contract is locked when
Android lands.
