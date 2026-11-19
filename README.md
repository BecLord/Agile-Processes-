# Scam Sheild: Human Voice Detection

Scam Shield is an Android application designed to help users identify and manage suspicious or scam calls. The app analyses voice recordings to estimate whether the speaker is a real human or an AI-generated voice, providing a dashboard, call-screening workflow, and local data handling.

This project was completed as part of our Agile Process module to learn how Agile project management works in practice.

## Problem

***"Make sure that it is a human behind the phone and not a bot."***

This project aims to create a barrier between potential cybercriminals and the person receiving the call by analysing voice recordings and identifying whether the speaker is likely to be human or AI-generated.

## Repository structure

```text
ScamSheild/
├── app/                         # Android application module
│   ├── src/                     # Kotlin source files, resources, manifest
│   ├── build.gradle.kts        # Module-level Gradle configuration
│   └── google-services.json    # Firebase configuration
├── python/                      # Python ML & dataset workspace
│   ├── dataset/                # Raw & processed audio data
│   ├── features/               # Feature extraction scripts & arrays
│   ├── models/                 # ML model scripts & exported models (.tflite/.onnx)
│   ├── preprocessing/          # Audio normalization & label encoding
│   ├── requirements.txt        # Python dependencies (librosa, numpy, scikit-learn)
│   └── run_pipeline.py         # Master script to run full data & feature pipeline
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

## Features

### Android Mobile App
- Suspicious call detection and call-screening workflow
- Landing and dashboard screens for user interaction
- Mobile user accounts, scam-call log, and admin dashboard / messaging
- Room database support for persisted call data
- Jetpack Compose-based UI

### Audio & Machine Learning
- Upload a voice recording for analysis
- Classify audio as **likely human**, **likely AI-generated**, or **inconclusive**
- Display a confidence score
- Compare machine-learning models
- Evaluate performance on noisy, compressed, and short audio

## How it Works

1. The user uploads an audio recording.
2. The app preprocesses the audio and extracts features.
3. The selected machine-learning model classifies the recording.
4. The app displays the result and confidence score.

*Note: The result is an estimate, not proof that a call is a scam.*

## Tech Stack

- Kotlin
- Android Jetpack Compose
- Room database
- Firebase integration
- Gradle
- Audio preprocessing & Machine Learning feature extraction

## Machine Learning

The project compares:

- **1** — uses 
- **2** — uses 

Both models are evaluated using accuracy, precision, recall, F1-score, and confusion matrices. The best-performing model is integrated into the mobile app.

## Dataset

The dataset contains genuine human speech and AI-generated voice recordings. Each recording includes its source, licence, consent status, speaker label, collection date, and class label.

## Getting Started

### Prerequisites

- **Android App:** Android Studio, JDK 17+, Android SDK
- **Python ML Pipeline:** Python 3.9+

### 1. Run the Android App

1. Clone the repository.
2. Open the project in Android Studio.
3. Sync Gradle files.
4. Select an Android emulator or connected device.
5. Run the app configuration.

Alternatively, build from the terminal:

```bash
./gradlew assembleDebug
```

### 2. Run the Python ML Data Pipeline

All Python scripts and data are contained within the [`python/`](file:///C:/Users/rlord/AndroidStudioProjects/Agile-Processes-/python) directory.

1. Install Python dependencies:
   ```bash
   pip install -r python/requirements.txt
   ```
2. Run the automated data preprocessing and feature extraction pipeline:
   ```bash
   python python/run_pipeline.py
   ```

This pipeline executes the following steps sequentially:
* **Audio Normalization:** Resamples audio to 16kHz & normalizes volume (`preprocessing/normalise_audio.py`).
* **Label Generation:** Creates and encodes CSV dataset labels (`preprocessing/create_labels.py` & `encode_labels.py`).
* **Feature Extraction:** Extracts 13 MFCC coefficients per frame (`features/extract_audio_features.py`).
* **Feature Standardization:** Pads/truncates features to 100 frames (`features/pad_truncate_features.py`).
* **Verification:** Validates structure and shape of feature arrays (`features/check_feature_structure.py`).

## Notes & Project Status

- The repository is organized so that Android code is isolated under `app/` while the root contains the project-level build configuration.
- Firebase configuration may need to be updated if the app is connected to a different project.
- This repository is currently structured as a mobile app prototype and is intended to be extended with additional detection logic, testing, and product documentation.

## Team

- Rebecca — Product Owner, Scrum Master (Sprint 3) and Developer
- Cassandra — Scrum Master (Sprint 1) and Developer
- Ibrahim — Scrum Master (Sprint 2) and Developer

