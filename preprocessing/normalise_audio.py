import librosa
import numpy as np
import soundfile as sf
from pathlib import Path

# Folder containing the original audio recordings
input_folder = Path("dataset/raw")

# Folder where processed recordings will be saved
output_folder = Path("dataset/processed")

# Create the output folder if it does not exist
output_folder.mkdir(parents=True, exist_ok=True)

# Find all WAV files in the input folder
audio_files = list(input_folder.glob("*.wav"))

if not audio_files:
    print("No WAV files found in dataset/raw")

for audio_file in audio_files:

    # Load audio as mono and resample to 16000 Hz
    audio, sample_rate = librosa.load(
        audio_file,
        sr=16000,
        mono=True
    )

    # Normalise audio volume
    max_amplitude = np.max(np.abs(audio))

    if max_amplitude > 0:
        audio = audio / max_amplitude

    # Save processed audio
    output_file = output_folder / audio_file.name

    sf.write(output_file, audio, sample_rate)

    print(f"Processed: {audio_file.name}")

print("Audio normalisation completed.")
