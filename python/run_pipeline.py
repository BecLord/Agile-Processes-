"""
Master Pipeline Script for BotDetector ML Audio Processing.

Executes the preprocessing, feature extraction, feature standardization,
and verification steps sequentially.
"""

import sys
import subprocess
from pathlib import Path

# Ensure working directory is set to the python/ folder
SCRIPT_DIR = Path(__file__).resolve().parent

PIPELINE_STEPS = [
    ("1. Normalise Audio", SCRIPT_DIR / "preprocessing" / "normalise_audio.py"),
    ("2. Create Labels CSV", SCRIPT_DIR / "preprocessing" / "create_labels.py"),
    ("3. Encode Categorical Labels", SCRIPT_DIR / "preprocessing" / "encode_labels.py"),
    ("4. Extract MFCC Audio Features", SCRIPT_DIR / "features" / "extract_audio_features.py"),
    ("5. Pad or Truncate Features", SCRIPT_DIR / "features" / "pad_truncate_features.py"),
    ("6. Verify Feature Structure", SCRIPT_DIR / "features" / "check_feature_structure.py"),
]

def run_pipeline():
    print("=" * 60)
    print("      BotDetector ML Data & Feature Extraction Pipeline      ")
    print("=" * 60)

    for title, script_path in PIPELINE_STEPS:
        print(f"\n---> Running Step: {title}")
        if not script_path.exists():
            print(f"Skipping (File not found): {script_path.name}")
            continue

        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=SCRIPT_DIR,
            text=True
        )

        if result.returncode != 0:
            print(f"FAILED: Step '{title}' exited with error code {result.returncode}")
            sys.exit(result.returncode)

    print("\n" + "=" * 60)
    print("Pipeline Execution Completed Successfully!")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
