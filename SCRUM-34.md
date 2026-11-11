# SCRUM-34: Assign Correct Labels to Human and AI-generated Voice Recordings

## Objective
Assign labels to human and AI-generated voice recordings
to prepare the dataset for the Scam Shield project.

## Dataset
The recordings were obtained from the group's shared dataset.

Current dataset:
- Human recordings: 30
- AI-generated recordings: 28
- Total recordings: 58

## Folder Structure
dataset/
    raw/
        human/
        ai_generated/
    labels.csv

## Implementation
Created preprocessing/create_labels.py to automatically
assign labels based on the recording folders.

Each recording is assigned one of two labels:
- human
- ai_generated

The labels are saved in dataset/labels.csv.

## Verification
Created preprocessing/verify_labels.py to check:
- Missing recordings
- Incorrect labels
- Duplicate entries
- Unlabelled recordings

Verification results:
- Missing files: 0
- Incorrect labels: 0
- Duplicate entries: 0
- Unlabelled files: 0

All 58 existing recordings passed the file and
folder-label consistency checks.

## Outstanding Work
- Obtain two additional AI-generated recordings.
- Confirm labels against the original recording sources.
- Re-run labelling and verification after adding recordings.
- Submit the work for peer review.

## Jira Reference
SCRUM-34