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
audio_files = list(input_folder.rglob("*.wav"))

if not audio_files:
    print("No WAV files found in dataset/raw")

for audio_file in audio_files:

    # Load audio as mono and resample to 16000 Hz
    audio, sample_rate = librosa.load(
        audio_file,
        sr=16000,
        mono=True
    )

    # SCRUM-30: Normalise audio to a target RMS level of -20 dBFS
    target_dbfs = -20

    # Calculate current RMS amplitude
    rms = np.sqrt(np.mean(audio ** 2))

    if rms > 0:
        # Convert target dBFS to linear amplitude
        target_rms = 10 ** (target_dbfs / 20)

        # Adjust audio volume towards the target
        audio = audio * (target_rms / rms)

        # Prevent clipping
        peak = np.max(np.abs(audio))
        if peak > 1.0:
            audio = audio / peak

    # Preserve the original category
    relative_path = audio_file.relative_to(input_folder)
    output_file = output_folder / relative_path
    output_file.parent.mkdir(parents=True, exist_ok=True)

    sf.write(output_file, audio, sample_rate)

    print(f"Processed: {audio_file.name}")

print("Audio normalisation completed.")

