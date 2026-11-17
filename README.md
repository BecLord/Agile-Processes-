# BotDetector

BotDetector is an Android application designed to help users identify and manage suspicious or scam calls. The app provides a simple dashboard, call-screening workflow, and local data handling to support scam detection and blocked-call reporting.

## Project purpose

This repository contains the Android client for a scam-call detection workflow. It is structured as a standard Gradle-based Android project, with application code grouped under the `app/` module and project configuration kept at the repository root.

## Repository structure

```text
BotDetector/
├── app/                         # Android application module
│   ├── src/                     # Kotlin source files, resources, manifest
│   ├── build.gradle.kts        # Module-level Gradle configuration
│   └── google-services.json    # Firebase configuration
├── gradle/                     # Gradle wrapper configuration
├── docs/                       # Project documentation
├── build.gradle.kts            # Root Gradle configuration
├── gradlew                     # Unix Gradle wrapper
├── gradlew.bat                 # Windows Gradle wrapper
├── gradle.properties          # Gradle settings
├── settings.gradle.kts         # Project settings
├── .gitignore                  # Git ignore rules
├── README.md                   # Project overview
└── .idea/                      # IDE metadata (local only)
```

## Key features

- Suspicious call detection workflow
- Landing and dashboard screens for user interaction
- Admin messaging and blocked-call tracking
- Room database support for persisted call data
- Jetpack Compose-based UI

## Tech stack

- Kotlin
- Android Jetpack Compose
- Room database
- Gradle
- Firebase integration

## Getting started

### Prerequisites

- Android Studio
- JDK 17 or later
- Android SDK configured for your environment

### Run the app

1. Clone the repository.
2. Open the project in Android Studio.
3. Sync Gradle files.
4. Select an Android emulator or connected device.
5. Run the app configuration.

Alternatively, from the terminal:

```bash
./gradlew assembleDebug
```

## Notes

- The repository is organized so that Android code is isolated under `app/` while the root contains the project-level build configuration.
- Firebase configuration may need to be updated if the app is connected to a different project.

## Project status

This repository is currently structured as a mobile app prototype and is intended to be extended with additional detection logic, testing, and product documentation.
