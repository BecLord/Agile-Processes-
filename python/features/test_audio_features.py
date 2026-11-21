# SCRUM-33: Transform Raw Data into Features
# SCRUM-180: Test feature files

import numpy as np
from pathlib import Path

# Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# Locate the saved feature file
feature_file = project_folder / "features" / "prepared" / "test_audio_features.npy"

# STEP 1: Load the saved feature file
if feature_file.exists():

    features = np.load(feature_file, allow_pickle=False)

    print("SCRUM-180: Feature file loaded successfully")
    print("File:", feature_file.name)

    # STEP 2: Check the expected feature values
    print("Feature shape:", features.shape)
    print("Number of frames:", features.shape[0])
    print("Number of features:", features.shape[1])

    # Check that 13 MFCC coefficients are present
    if features.ndim == 2 and features.shape[0] > 0 and features.shape[1] == 13:
        print("PASS: 13 MFCC coefficients found")
    else:
        print("FAIL: Unexpected feature shape")

    # Check for invalid values
    if np.isfinite(features).all():
        print("PASS: All feature values are valid")
    else:
        print("FAIL: Invalid feature values found")

    # STEP 3: Confirm suitability for the next stage
    if (
        features.ndim == 2
        and features.shape[0] > 0
        and features.shape[1] == 13
        and np.isfinite(features).all()
    ):
        print("SCRUM-180: Feature file passed validation")
        print("Feature file is ready for the next stage")
    else:
        print("SCRUM-180: Feature file failed validation")

else:
    print("SCRUM-180: Feature file not found")