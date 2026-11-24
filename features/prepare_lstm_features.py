# SCRUM-192: Prepare Features for LSTM

import numpy as np
from pathlib import Path

# Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# Input and output folders
input_folder = project_folder / "features" / "standardised"
output_folder = project_folder / "features" / "lstm"

# Create output folder
output_folder.mkdir(parents=True, exist_ok=True)

# Required LSTM feature dimensions
TARGET_SHAPE = (100, 13)

# Find standardised MFCC files
feature_files = sorted(
    file for file in input_folder.glob("*_features.npy")
    if file.name.startswith(("human_", "ai_generated_"))
)

print("SCRUM-192: Prepare Features for LSTM")
print("Total feature files:", len(feature_files))

# Load and validate the features
lstm_features = []

for feature_file in feature_files:

    features = np.load(feature_file, allow_pickle=False)

    # Check feature dimensions
    if features.shape != TARGET_SHAPE:
        raise ValueError(
            f"Incorrect feature dimensions: {feature_file.name}"
        )

    # Check for invalid values
    if not np.isfinite(features).all():
        raise ValueError(
            f"Invalid values found: {feature_file.name}"
        )

    # Add recording to LSTM dataset
    lstm_features.append(features)

# Check that recordings were found
if not lstm_features:
    raise ValueError("No standardised feature files found.")

# Combine recordings into a 3D array
X_lstm = np.stack(lstm_features, axis=0)

# Verify LSTM input dimensions
expected_shape = (len(feature_files), 100, 13)

if X_lstm.shape != expected_shape:
    raise ValueError("Incorrect LSTM input shape.")

# Save prepared LSTM features
output_file = output_folder / "X_lstm.npy"
np.save(output_file, X_lstm)

print("\nSCRUM-192: Processing Summary")
print("Successfully prepared:", len(feature_files))
print("LSTM input shape:", X_lstm.shape)
print("Saved to:", output_file)
print("SCRUM-192: LSTM features prepared successfully!")