# SCRUM-193: Prepare Features for CNN

import numpy as np
from pathlib import Path

# Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# Input and output folders
input_folder = project_folder / "features" / "standardised"
output_folder = project_folder / "features" / "cnn"

# Create the CNN output folder
output_folder.mkdir(parents=True, exist_ok=True)

# Required feature dimensions
TARGET_SHAPE = (100, 13)

# Find all standardised MFCC feature files
feature_files = sorted(
    file for file in input_folder.glob("*_features.npy")
    if file.name.startswith(("human_", "ai_generated_"))
)

cnn_features = []
error_count = 0

print("SCRUM-193: Prepare Features for CNN")
print("Total feature files:", len(feature_files))

# Process each feature file
for feature_file in feature_files:

    try:
        # Load MFCC features
        features = np.load(feature_file, allow_pickle=False)

        # Check feature dimensions
        if features.shape != TARGET_SHAPE:
            print("FAIL: Incorrect shape:", feature_file.name)
            error_count += 1
            continue

        # Check for invalid values
        if not np.issubdtype(features.dtype, np.number):
            print("FAIL: Non-numeric features:", feature_file.name)
            error_count += 1
            continue

        if not np.isfinite(features).all():
            print("FAIL: Invalid values:", feature_file.name)
            error_count += 1
            continue

        # Add channel dimension for CNN
        cnn_feature = np.expand_dims(features, axis=-1)

        cnn_features.append(cnn_feature)

        print("PASS:", feature_file.name, cnn_feature.shape)

    except Exception as error:
        print("ERROR:", feature_file.name, error)
        error_count += 1

# Save only when all 58 files are valid
if len(feature_files) == 58 and len(cnn_features) == 58 and error_count == 0:

    X_cnn = np.stack(cnn_features)

    output_file = output_folder / "X_cnn.npy"

    np.save(output_file, X_cnn)

    print("\nSCRUM-193: Processing Summary")
    print("Successfully prepared:", len(cnn_features))
    print("CNN input shape:", X_cnn.shape)
    print("Saved to:", output_file)
    print("SCRUM-193: CNN features prepared successfully!")

else:
    print("\nSCRUM-193: Preparation incomplete.")
    print("Successfully prepared:", len(cnn_features))
    print("Errors:", error_count)