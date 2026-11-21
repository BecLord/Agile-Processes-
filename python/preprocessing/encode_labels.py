import csv
from pathlib import Path

# SCRUM-31: Encode Categorical Values

# Locate the project dataset
project_folder = Path(__file__).resolve().parent.parent
csv_file = project_folder / "dataset" / "labels.csv"

# Define numerical labels
label_mapping = {
    "human": 0,
    "ai_generated": 1
}

# Read the existing CSV file
with open(csv_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# Convert categorical labels into numerical values
for row in rows:
    label = row["label"]

    if label not in label_mapping:
        raise ValueError(f"Unknown label: {label}")

    row["encodedLabel"] = label_mapping[label]

# Save the updated CSV file
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["filename", "label", "encodedLabel"]
    )

    writer.writeheader()
    writer.writerows(rows)

print("SCRUM-31: Categorical encoding completed successfully.")
print(f"Total recordings encoded: {len(rows)}")
print("Human = 0")
print("AI-generated = 1")
print("Updated file: dataset/labels.csv")