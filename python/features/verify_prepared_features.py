# SCRUM-35: Verify Prepared Audio Features

import numpy as np
from pathlib import Path

# Locate the prepared features file
project_folder = Path(__file__).resolve().parent.parent

feature_file = project_folder / "features" / "prepared" / "prepared_features.npy"

# Load the prepared features
features = np.load(feature_file)

print("SCRUM-35: Prepared Feature Verification")

print("Dataset shape:", features.shape)
print("Number of samples:", features.shape[0])
print("Frames per sample:", features.shape[1])
print("Features per frame:", features.shape[2])

# Verify dimensions
assert features.shape == (3, 100, 13), "Incorrect feature dimensions"

# Check for invalid values
assert np.isfinite(features).all(), "Invalid values found"

print("All prepared features have consistent dimensions.")
print("No invalid values found.")
print("SCRUM-35: Verification completed successfully.")