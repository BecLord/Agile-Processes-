
# SCRUM-190: Pad or Truncate Features

import numpy as np
from pathlib import Path

# Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# Locate the extracted MFCC features
input_folder = project_folder / "features" / "prepared"

# Create a separate folder for standardised features
output_folder = project_folder / "features" / "standardised"
output_folder.mkdir(parents=True, exist_ok=True)

# Required feature dimensions
TARGET_FRAMES = 100
TARGET_MFCC = 13

# Find the extracted recording feature files
feature_files = sorted(
    file for file in input_folder.glob("*_features.npy")
    if file.name.startswith(("human_", "ai_generated_"))
)

processed_count = 0
error_count = 0

print("SCRUM-190: Pad or Truncate Features")
print("Total feature files:", len(feature_files))

# Process each extracted feature file
for feature_file in feature_files:

    try:
        features = np.load(feature_file, allow_pickle=False)

        # Check the original feature dimensions
        if features.ndim != 2 or features.shape[1] != TARGET_MFCC:
            raise ValueError("Expected 13 MFCC coefficients")

        if features.shape[0] == 0 or not np.isfinite(features).all():
            raise ValueError("Empty or invalid feature values")

        current_frames = features.shape[0]

        # Pad recordings shorter than 100 frames
        if current_frames < TARGET_FRAMES:

            padding = TARGET_FRAMES - current_frames

            features = np.pad(
                features,
                ((0, padding), (0, 0)),
                mode="constant"
            )

            action = "Padded"

        # Truncate recordings longer than 100 frames
        elif current_frames > TARGET_FRAMES:

            features = features[:TARGET_FRAMES, :]

            action = "Truncated"

        else:
            action = "Already correct"

        # Check the final feature dimensions
        if features.shape != (TARGET_FRAMES, TARGET_MFCC):
            raise ValueError("Incorrect final feature size")

        # Save standardised features
        output_file = output_folder / feature_file.name
        np.save(output_file, features)

        # Verify the saved file
        saved_features = np.load(output_file, allow_pickle=False)

        if saved_features.shape != (TARGET_FRAMES, TARGET_MFCC):
            raise ValueError("Saved feature size is incorrect")

        processed_count += 1

        print(
            feature_file.name,
            "Original frames:", current_frames,
            "Action:", action,
            "Final shape:", saved_features.shape
        )

    except Exception as error:
        error_count += 1
        print("ERROR:", feature_file.name, error)

# Display the results
print("\nSCRUM-190: Processing Summary")
print("Successfully processed:", processed_count)
print("Errors:", error_count)
print("Output folder:", output_folder)

if processed_count == len(feature_files) and error_count == 0 and processed_count > 0:
    print("SCRUM-190: All features standardised successfully!")
else:
    print("SCRUM-190: Some features require attention.")
