import csv
from pathlib import Path
from collections import Counter

# Dataset locations
dataset_folder = Path("dataset")
raw_folder = dataset_folder / "raw"
labels_file = dataset_folder / "labels.csv"

# Read the CSV file
with open(labels_file, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    records = list(reader)

# Count the labels
labels = [record["label"] for record in records]
counts = Counter(labels)

print("=== SCRUM-34 Dataset Verification ===")

print("Total recordings labelled:", len(records))
print("Human recordings:", counts["human"])
print("AI-generated recordings:", counts["ai_generated"])

# Check each recording
missing_files = []
incorrect_labels = []
duplicate_files = []
seen_files = set()

for record in records:
    filename = record["filename"]
    label = record["label"]

    audio_file = raw_folder / filename

    # Check whether the recording exists
    if not audio_file.is_file():
        missing_files.append(filename)

    # Check whether the label matches the folder
    expected_label = Path(filename).parent.name

    if label != expected_label or label not in ("human", "ai_generated"):
        incorrect_labels.append(filename)

    # Check duplicate entries
    if filename in seen_files:
        duplicate_files.append(filename)

    seen_files.add(filename)

# Check whether any WAV files were left out of the CSV
actual_files = {
    file.relative_to(raw_folder).as_posix()
    for folder in ("human", "ai_generated")
    for file in (raw_folder / folder).glob("*.wav")
}

unlabelled_files = actual_files - seen_files

print("\n=== Verification Results ===")

print("Missing files:", len(missing_files))
print("Incorrect labels:", len(incorrect_labels))
print("Duplicate entries:", len(duplicate_files))
print("Unlabelled files:", len(unlabelled_files))

if missing_files:
    print("Missing:", missing_files)

if incorrect_labels:
    print("Incorrect:", incorrect_labels)

if duplicate_files:
    print("Duplicates:", duplicate_files)

if unlabelled_files:
    print("Unlabelled:", sorted(unlabelled_files))

# Final verification
if not missing_files and not incorrect_labels and not duplicate_files and not unlabelled_files:
    print("\nPASS: All existing recordings are labelled correctly.")
else:
    print("\nFAIL: Dataset verification found problems.")

# Check Jira minimum dataset requirement
if counts["human"] >= 30 and counts["ai_generated"] >= 30:
    print("PASS: Minimum 30 recordings per category achieved.")
else:
    print("PENDING: Minimum 30 recordings per category not yet achieved.")