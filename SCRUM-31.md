# SCRUM-31: Encode Categorical Values

## Objective

Convert categorical voice recording labels into numerical
values so that they can be processed by the machine
learning model.

## Dataset

The dataset contains 58 labelled voice recordings.

- Human recordings: 30
- AI-generated recordings: 28
- Total recordings: 58

## Numerical Encoding

The following numerical labels were assigned:

- human = 0
- ai_generated = 1

## Implementation

Created preprocessing/encode_labels.py to convert
categorical labels into numerical values.

The script reads dataset/labels.csv and adds a new
column called encodedLabel.

The updated CSV contains three columns:

- filename
- label
- encodedLabel

## Verification

Created preprocessing/verify_encoding.py to verify
that all numerical labels are correct.

Verification results:

- Total recordings: 58
- Human recordings (0): 30
- AI-generated recordings (1): 28
- All numerical labels verified successfully.

## CSV Loading Test

Created preprocessing/test_encoded_labels.py to
confirm that numerical labels can be loaded
and converted into integers.

Test results:

- CSV loaded successfully.
- All 58 recordings loaded.
- All numerical labels are valid.
- No errors occurred.

## Jira Reference

SCRUM-31 - Encode Categorical Values

## Status

Implementation and standalone verification completed
successfully.

The encoded labels are ready for integration with the
machine learning training script.

Full integration testing will be performed when the
training script becomes available.