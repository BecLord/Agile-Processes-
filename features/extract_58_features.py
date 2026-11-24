# SCRUM-33: Transform Raw Audio Data into Features
# Scam Shield - Agile Processes Project
# Extract MFCC features from human and AI-generated recordings

import csv
from pathlib import Path

import librosa
import numpy as np


# --------------------------------------------------
# Step 1: Locate project folders
# --------------------------------------------------

project_folder = Path(__file__).resolve().parent.parent

dataset_folder = project_folder / "dataset"
labels_file = dataset_folder / "labels.csv"

output_folder = project_folder / "features" / "model_ready"

output_folder.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Step 2: Load the existing labels
# --------------------------------------------------

with open(labels_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    recordings = list(reader)


print("SCRUM-33: Audio Feature Extraction")
print("Total labelled recordings:", len(recordings))


# --------------------------------------------------
# Step 3: Prepare feature and label lists
# --------------------------------------------------

all_features = []
all_labels = []
all_filenames = []

errors = []


# --------------------------------------------------
# Step 4: Process each audio recording
# --------------------------------------------------

for recording in recordings:

    filename = recording["filename"]

    label = recording["label"]

    encoded_label = int(recording["encodedLabel"])

    audio_file = dataset_folder / "raw" / filename

    print("\nProcessing:", filename)

    # Check that the file exists
    if not audio_file.is_file():
        print("ERROR: Audio file not found")
        errors.append(filename)
        continue

    try:

        # Load the audio recording
        audio, sample_rate = librosa.load(
            audio_file,
            sr=16000,
            mono=True
        )

        if len(audio) == 0:
            raise ValueError("Audio recording is empty")

        # Extract 13 MFCC features
        mfcc = librosa.feature.mfcc(
            y=audio,
            sr=sample_rate,
            n_mfcc=13
        )

        # Calculate mean and standard deviation
        mfcc_mean = np.mean(mfcc, axis=1)

        mfcc_std = np.std(mfcc, axis=1)

        # Combine into 26 features
        features = np.concatenate(
            (mfcc_mean, mfcc_std)
        )

        if not np.isfinite(features).all():
            raise ValueError("Features contain invalid values")

        # Store features and corresponding label
        all_features.append(features)

        all_labels.append(encoded_label)

        all_filenames.append(filename)

        print("PASS: Features extracted:", features.shape)

    except Exception as error:

        print("FAIL:", error)

        errors.append(filename)


# --------------------------------------------------
# Step 5: Check processing results
# --------------------------------------------------

print("\nSCRUM-33: Processing Summary")

print("Successfully processed:", len(all_features))

print("Errors:", len(errors))


# --------------------------------------------------
# Step 6: Save the extracted features
# --------------------------------------------------

if len(errors) == 0 and len(all_features) == len(recordings) and len(recordings) == 58:

    X = np.array(all_features)

    y = np.array(all_labels)

    np.save(output_folder / "X_features.npy", X)

    np.save(output_folder / "y_labels.npy", y)

    # Save filenames to preserve feature-label alignment
    with open(
        output_folder / "feature_mapping.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(["filename", "encodedLabel"])

        for filename, label in zip(all_filenames, all_labels):
            writer.writerow([filename, label])

    print("\nFeature dataset shape:", X.shape)

    print("Labels shape:", y.shape)

    print("Human samples:", np.sum(y == 0))

    print("AI-generated samples:", np.sum(y == 1))

    print("\nSCRUM-33: Feature extraction completed successfully!")

else:

    print("\nSCRUM-33: Processing incomplete.")

    print("Check the missing or failed recordings above.")

    print("Existing model-ready files have not been overwritten.")