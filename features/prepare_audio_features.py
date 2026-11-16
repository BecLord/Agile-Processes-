# SCRUM-35: Prepare Audio Features in a Consistent Size and Structure

import numpy as np
from pathlib import Path

# Set the required number of time frames for each audio feature
TARGET_FRAMES = 100

# Create the folder where prepared features will be saved
output_folder = Path("features/prepared")
output_folder.mkdir(parents=True, exist_ok=True)

# Create sample audio features with different lengths
# Each sample contains 13 feature values per time frame
sample_features = [
    np.random.default_rng(1).random((80, 13)),
    np.random.default_rng(2).random((100, 13)),
    np.random.default_rng(3).random((120, 13))
]

prepared_features = []

# Prepare each audio feature array
for index, features in enumerate(sample_features):

    print(f"Sample {index + 1} original shape: {features.shape}")

    # Check the number of time frames
    current_frames = features.shape[0]

    if current_frames < TARGET_FRAMES:

        # Add zeros when the recording is too short
        padding = TARGET_FRAMES - current_frames

        features = np.pad(
            features,
            ((0, padding), (0, 0)),
            mode="constant"
        )

    elif current_frames > TARGET_FRAMES:

        # Remove extra frames when the recording is too long
        features = features[:TARGET_FRAMES, :]

    # Store the prepared feature array
    prepared_features.append(features)

    print(f"Sample {index + 1} prepared shape: {features.shape}")

# Combine the prepared features into one NumPy array
prepared_features = np.array(prepared_features)

# Save the prepared features
output_file = output_folder / "prepared_features.npy"
np.save(output_file, prepared_features)

print("\nSCRUM-35: Feature preparation completed successfully.")
print(f"Final dataset shape: {prepared_features.shape}")
print(f"Prepared features saved to: {output_file}")