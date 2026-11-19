
# SCRUM-33: Transform Raw Data into Features
# STEP 5: Load preprocessed audio

import librosa
from pathlib import Path

# Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# Locate the preprocessed audio recording
audio_file = project_folder / "dataset" / "processed" / "human" / "1495.wav"

# Check whether the recording exists
if audio_file.exists():

    # Load audio without changing its original sample rate
    audio, sample_rate = librosa.load(audio_file, sr=None)

    # Calculate recording duration
    duration = len(audio) / sample_rate

    print("SCRUM-176: Audio loaded successfully")
    print("File:", audio_file.name)
    print("Sample rate:", sample_rate, "Hz")
    print("Duration:", round(duration, 2), "seconds")
    print("Number of samples:", len(audio))

# SCRUM-177: Extract MFCC features from audio

    # Extract 13 MFCC coefficients
    mfcc_features = librosa.feature.mfcc(
        y=audio,
        sr=sample_rate,
        n_mfcc=13
    )

    # Transpose to arrange data as (time frames, features)
    mfcc_features = mfcc_features.T

    print("\nSCRUM-177: MFCC extraction completed")
    print("MFCC feature shape:", mfcc_features.shape)
    print("Number of frames:", mfcc_features.shape[0])
    print("Features per frame:", mfcc_features.shape[1])


    # SCRUM-178: Save extracted features

    import numpy as np

    # Folder for saving extracted features
    output_folder = project_folder / "features" / "prepared"
    output_folder.mkdir(parents=True, exist_ok=True)

    # Save MFCC features
    output_file = output_folder / f"{audio_file.parent.name}_{audio_file.stem}_features.npy"
    np.save(output_file, mfcc_features)

    print("\nSCRUM-178: Features saved successfully")
    print("Saved file:", output_file)

    # Load saved features to verify
    loaded_features = np.load(output_file)

    print("Loaded feature shape:", loaded_features.shape)
    print("Saved data matches original:", np.array_equal(mfcc_features, loaded_features))


    # SCRUM-179: Link features to recording IDs and class labels

    import csv

    # Use the recording filename as its ID
    recording_id = audio_file.stem

    # Locate the dataset labels
    labels_file = project_folder / "dataset" / "labels.csv"

    # Find the class label for this recording
    class_label = None

    with open(labels_file, "r", newline="") as file:
        reader = csv.DictReader(file)

        relative_audio_path = audio_file.relative_to(
            project_folder / "dataset" / "processed"
        ).as_posix()

        for row in reader:
            labelled_filename = Path(row["filename"]).as_posix()

            if labelled_filename == relative_audio_path:
                if class_label is not None:
                    raise ValueError(
                        "Multiple label entries match this recording"
                    )

                class_label = row["label"]
    # Do not assign a label unless it can be verified
    if class_label is None:
        print("\nSCRUM-179: No matching class label found")
        print("Recording:", audio_file.name)
        print("Add a verified label before creating the mapping.")

    else:
        # Save recording ID, audio file, feature file and class label
        mapping_file = output_folder / "feature_mapping.csv"

        with open(mapping_file, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "recording_id",
                "audio_file",
                "feature_file",
                "class_label"
            ])

            writer.writerow([
                recording_id,
                audio_file.name,
                output_file.name,
                class_label
            ])

        print("\nSCRUM-179: Features linked successfully")
        print("Recording ID:", recording_id)
        print("Audio file:", audio_file.name)
        print("Feature file:", output_file.name)
        print("Class label:", class_label)
        print("Mapping saved:", mapping_file)

else:
    print("Audio file not found:", audio_file)