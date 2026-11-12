import csv
from pathlib import Path

# Folder containing the recordings
dataset_folder = Path("dataset/raw")

# CSV file to save the labels
output_file = Path("dataset/labels.csv")

# Categories and their labels
categories = {
    "human": "human",
    "ai_generated": "ai_generated"
}

# Create the CSV file
with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Column headings
    writer.writerow(["filename", "label"])

    # Read recordings from each category
    for folder_name, label in categories.items():
        folder = dataset_folder / folder_name

        for audio_file in sorted(folder.glob("*.wav")):
            filename = f"{folder_name}/{audio_file.name}"
            writer.writerow([filename, label])

            print(f"Labelled: {filename} -> {label}")

print("Audio labelling completed.")