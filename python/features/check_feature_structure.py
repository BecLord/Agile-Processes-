
# SCRUM-191: Check All Features Have the Same Structure

import numpy as np
from pathlib import Path

# Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# Locate the standardised feature files
input_folder = project_folder / "features" / "standardised"

# Required feature dimensions
TARGET_SHAPE = (100, 13)

# Find the standardised recording feature files
feature_files = sorted(
    file for file in input_folder.glob("*_features.npy")
    if file.name.startswith(("human_", "ai_generated_"))
)

checked_count = 0
error_count = 0

print("SCRUM-191: Check Feature Structure")
print("Total feature files:", len(feature_files))

# Check each feature file
for feature_file in feature_files:

    try:
        # Load the standardised features
        features = np.load(feature_file, allow_pickle=False)

        # Check feature dimensions
        if features.shape != TARGET_SHAPE:
            print("FAIL: Incorrect shape:", feature_file.name, features.shape)
            error_count += 1
            continue

        # Check that features contain numerical values
        if not np.issubdtype(features.dtype, np.number):
            print("FAIL: Non-numeric features:", feature_file.name)
            error_count += 1
            continue

        # Check for invalid values
        if not np.isfinite(features).all():
            print("FAIL: Invalid values:", feature_file.name)
            error_count += 1
            continue

        checked_count += 1
        print("PASS:", feature_file.name, features.shape)

    except Exception as error:
        print("ERROR:", feature_file.name, error)
        error_count += 1

# Display verification results
print("\nSCRUM-191: Verification Summary")
print("Successfully checked:", checked_count)
print("Errors:", error_count)

if len(feature_files) == 58 and checked_count == 58 and error_count == 0:
    print("SCRUM-191: All 58 features have the same structure!")
else:
    print("SCRUM-191: Feature verification requires attention.")
