# Official Sources for mobile-craft

Ground every non-obvious technical claim in these sources. Community sources (blogs, Stack
Overflow, Reddit) are non-authoritative and may be used only as implementation inspiration.

## Apple platforms

- [Apple Developer Documentation](https://developer.apple.com/documentation/) — root.
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines).
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/).
- [App Privacy Details on the App Store](https://developer.apple.com/app-store/app-privacy-details/) —
  Apple Privacy Labels guidance.
- [App Store Connect Help](https://developer.apple.com/help/app-store-connect/).
- [Universal Links](https://developer.apple.com/documentation/xcode/supporting-universal-links-in-your-app).
- [LocalAuthentication](https://developer.apple.com/documentation/localauthentication) — Touch
  ID / Face ID / Optic ID + passcode fallback.
- [BackgroundTasks](https://developer.apple.com/documentation/backgroundtasks) —
  BGAppRefreshTask + BGProcessingTask.
- [User Notifications](https://developer.apple.com/documentation/usernotifications) — APNs +
  UNUserNotificationCenter.
- [App Intents](https://developer.apple.com/documentation/appintents).
- [WidgetKit](https://developer.apple.com/documentation/widgetkit).
- [Live Activities](https://developer.apple.com/documentation/activitykit).
- [StoreKit 2](https://developer.apple.com/documentation/storekit).
- [HealthKit](https://developer.apple.com/documentation/healthkit).
- [ARKit](https://developer.apple.com/documentation/arkit) +
  [RealityKit](https://developer.apple.com/documentation/realitykit).

For deep Apple-platform implementation, hand off to `ios-craft`.

## Android

- [Android Developer Documentation](https://developer.android.com/).
- [Material Design 3 Specification](https://m3.material.io/) — dynamic color, predictive
  back, edge-to-edge, navigation patterns.
- [Jetpack Compose Documentation](https://developer.android.com/jetpack/compose).
- [App Links](https://developer.android.com/training/app-links).
- [WorkManager](https://developer.android.com/topic/libraries/architecture/workmanager).
- [BiometricPrompt](https://developer.android.com/training/sign-in/biometric-auth) — Class 3
  vs Class 2 tiers + device-credential fallback.
- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging).
- [Play Console Help](https://support.google.com/googleplay/android-developer).
- [Data Safety form guidance](https://support.google.com/googleplay/android-developer/answer/10787469).
- [Doze and App Standby](https://developer.android.com/training/monitoring-device-state/doze-standby) —
  background work limits.

## React Native + Expo

- [React Native Documentation](https://reactnative.dev/docs/getting-started).
- [React Native New Architecture](https://reactnative.dev/docs/the-new-architecture/landing-page) —
  TurboModules, Fabric, Codegen.
- [Expo Documentation](https://docs.expo.dev/).
- [EAS Build](https://docs.expo.dev/build/introduction/).
- [EAS Update](https://docs.expo.dev/eas-update/introduction/) — OTA update mechanics with
  channels.
- [expo-notifications](https://docs.expo.dev/versions/latest/sdk/notifications/).
- [expo-local-authentication](https://docs.expo.dev/versions/latest/sdk/local-authentication/).
- [expo-task-manager](https://docs.expo.dev/versions/latest/sdk/task-manager/) +
  [expo-background-fetch](https://docs.expo.dev/versions/latest/sdk/background-fetch/).
- [expo-linking](https://docs.expo.dev/versions/latest/sdk/linking/) — deep link handling.

For deep RN/Expo implementation, hand off to `react-native-foundations` and `expo`.

## Flutter

- [Flutter Documentation](https://docs.flutter.dev/).
- [Dart Language Tour](https://dart.dev/language).
- [Flutter packages](https://pub.dev/) — `local_auth`, `firebase_messaging`, `workmanager`,
  `drift`, `isar`.

## Cross-platform design references

- [Apple HIG vs Material Design comparison](https://m3.material.io/) — Material 3 explicitly
  documents where it differs from Apple HIG; useful for understanding what shouldn't be
  copy-pasted between platforms.

## Privacy + compliance

- [Apple App Privacy Details on the App Store](https://developer.apple.com/app-store/app-privacy-details/).
- [Play Console Data Safety section](https://support.google.com/googleplay/android-developer/answer/10787469).
- [GDPR compliance for mobile apps](https://gdpr.eu/) — applies to both platforms when
  shipping in the EU.
- [Apple Privacy Manifests](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files) —
  required disclosure of API usage in iOS 17+.

## Source hierarchy

1. Apple Developer Documentation + Apple HIG for iOS / iPadOS / macOS / visionOS / watchOS /
   tvOS questions.
2. Android Developer Documentation + Material 3 spec for Android questions.
3. Expo / React Native / Flutter official docs for cross-platform questions.
4. Apple Review Guidelines and Play Console Help for store-policy questions.
5. Privacy guidance from both Apple and Google for disclosure questions.
6. Community examples — labeled non-authoritative.

If official docs conflict with anything in this skill, follow the official docs and update
this file with the change. Open a PR with a one-line note in the changelog.
