# SCRUM-33: Transform Raw Data into Features
# STEP 5: Load preprocessed audio

import librosa
import numpy as np
import csv
from pathlib import Path

# Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# Locate the preprocessed audio recordings
input_folder = project_folder / "dataset" / "processed"

# Locate the dataset labels
labels_file = project_folder / "dataset" / "labels.csv"

# Folder for saving extracted features
output_folder = project_folder / "features" / "prepared"
output_folder.mkdir(parents=True, exist_ok=True)

# File for linking features to recordings
mapping_file = output_folder / "feature_mapping.csv"

# Read recording labels
with open(labels_file, "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    recordings = list(reader)

# Store recording information
feature_mapping = []

processed_count = 0
error_count = 0

print("SCRUM-33: Transform Raw Data into Features")
print("Total labelled recordings:", len(recordings))

# Process each labelled audio recording
for row in recordings:

    recording_path = Path(row["filename"])
    class_label = row["label"].strip()

    # Verify the class label
    if class_label not in ["human", "ai_generated"]:
        print("Invalid class label:", recording_path)
        error_count += 1
        continue

    # Verify the recording folder matches its label
    if recording_path.parent.as_posix() != class_label:
        print("Folder and label do not match:", recording_path)
        error_count += 1
        continue

    audio_file = input_folder / recording_path

    # Check whether the recording exists
    if not audio_file.exists():
        print("Audio file not found:", audio_file)
        error_count += 1
        continue

    try:
        # SCRUM-176: Load preprocessed audio

        # Load audio without changing its sample rate
        audio, sample_rate = librosa.load(audio_file, sr=None)

        # Calculate recording duration
        duration = len(audio) / sample_rate

        # SCRUM-177: Extract MFCC features from audio

        # Extract 13 MFCC coefficients
        mfcc_features = librosa.feature.mfcc(
            y=audio,
            sr=sample_rate,
            n_mfcc=13
        )

        # Transpose to arrange data as (time frames, features)
        mfcc_features = mfcc_features.T

        # SCRUM-178: Save extracted features

        output_file = output_folder / (
            f"{class_label}_{audio_file.stem}_features.npy"
        )

        np.save(output_file, mfcc_features)

        # Load saved features to verify
        loaded_features = np.load(output_file)

        if not np.array_equal(mfcc_features, loaded_features):
            raise ValueError("Saved features do not match")

        # SCRUM-179: Link features to recording IDs and labels

        recording_id = audio_file.stem

        feature_mapping.append([
            recording_id,
            recording_path.as_posix(),
            output_file.name,
            class_label,
            round(duration, 2),
            mfcc_features.shape[0],
            mfcc_features.shape[1]
        ])

        processed_count += 1

        print("Processed:", recording_path)
        print("MFCC feature shape:", mfcc_features.shape)

    except Exception as error:
        print("Error processing:", recording_path)
        print("Reason:", error)
        error_count += 1

# SCRUM-179: Save recording and feature mapping

with open(mapping_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "recording_id",
        "audio_file",
        "feature_file",
        "class_label",
        "duration_seconds",
        "number_of_frames",
        "features_per_frame"
    ])

    writer.writerows(feature_mapping)

# Display processing results
print("\nSCRUM-33: Feature extraction summary")
print("Total labelled recordings:", len(recordings))
print("Successfully processed:", processed_count)
print("Errors:", error_count)
print("Feature mapping saved:", mapping_file)

if processed_count == len(recordings) and error_count == 0:
    print("SCRUM-33: All labelled recordings processed successfully!")
else:
    print("SCRUM-33: Some recordings require attention.")