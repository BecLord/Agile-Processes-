import csv
from pathlib import Path

# SCRUM-31: Test loading numerical labels for model training

# Locate the dataset
project_folder = Path(__file__).resolve().parent.parent
csv_file = project_folder / "dataset" / "labels.csv"

# Read encoded labels
with open(csv_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# Convert encoded labels into integers
labels = []

for row in rows:
    encoded_label = int(row["encodedLabel"])
    labels.append(encoded_label)

# Check the labels
assert len(labels) == 58, "Unexpected number of recordings"
assert all(label in (0, 1) for label in labels), "Invalid numerical label"

# Display results
print("SCRUM-31: CSV loading test successful.")
print(f"Total recordings loaded: {len(labels)}")
print(f"Human recordings (0): {labels.count(0)}")
print(f"AI-generated recordings (1): {labels.count(1)}")
print("All numerical labels can be loaded as integers.")