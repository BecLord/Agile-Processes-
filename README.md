# Agile-Processes-

## SCRUM-33: Transform Raw Data into Features

### SCRUM-175: Select Feature Extraction Method

The selected feature extraction method is
Mel-Frequency Cepstral Coefficients (MFCC).

The project uses the Python librosa library to extract
13 MFCC coefficients from audio recordings.

MFCC features represent characteristics of audio
signals and can be used as input for machine learning models.

The extracted features are saved as NumPy (.npy) files
inside the features/prepared folder.

Feature extraction method: MFCC
Number of coefficients: 13
Python library: librosa
Output format: .npy

### SCRUM-33: Feature Extraction Results

The audio preprocessing and feature extraction tasks were completed successfully.

- Total labelled audio recordings: 58
- Human voice recordings: 30
- AI-generated voice recordings: 28
- Audio sample rate: 16,000 Hz
- Feature extraction method: MFCC
- Number of MFCC coefficients: 13
- Successfully processed recordings: 58
- Processing errors: 0

The extracted features were saved in the features/prepared folder as NumPy (.npy) files.

A feature_mapping.csv file was created to link each audio recording to its extracted features and class label.

All 58 labelled recordings were successfully processed and verified.
