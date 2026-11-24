import csv
from pathlib import Path

# SCRUM-31: Verify Categorical Encoding

project_folder = Path(__file__).resolve().parent.parent
csv_file = project_folder / "dataset" / "labels.csv"

label_mapping = {
    "human": 0,
    "ai_generated": 1
}

with open(csv_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    required_columns = {"filename", "label", "encodedLabel"}

    if not required_columns.issubset(reader.fieldnames or []):
        raise ValueError("Required CSV columns are missing.")

    rows = list(reader)

human_count = 0
ai_count = 0

for row in rows:
    label = row["label"]
    encoded = row["encodedLabel"]

    if label not in label_mapping:
        raise ValueError(f"Unknown label: {label}")

    if not row["filename"]:
        raise ValueError("Missing recording filename.")

    if encoded != str(label_mapping[label]):
        raise ValueError(
            f"Incorrect encoding for {row['filename']}"
        )

    if label == "human":
        human_count += 1
    else:
        ai_count += 1

print("SCRUM-31: Encoding verification successful.")
print(f"Total recordings: {len(rows)}")
print(f"Human recordings (0): {human_count}")
print(f"AI-generated recordings (1): {ai_count}")
print("All numerical labels are correct.")
print("CSV loaded successfully.")