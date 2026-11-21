# Agile Processes - Scam Shield Project
# Test Google Cloud Speech-to-Text with three human recordings

from google.cloud import speech
from pathlib import Path
import subprocess

# Three human voice recordings
recordings = ["1001.wav", "1002.wav", "1011.wav"]

# Folder locations
input_folder = Path("dataset/raw/Human")
output_folder = Path("dataset/processed")

output_folder.mkdir(parents=True, exist_ok=True)

# Create Google Cloud Speech-to-Text client
client = speech.SpeechClient()

for filename in recordings:

    print("\nProcessing:", filename)

    input_file = input_folder / filename

    converted_file = output_folder / f"{Path(filename).stem}_converted.wav"

    transcription_file = output_folder / f"{Path(filename).stem}_transcription.txt"

    if not input_file.exists():
        print("Recording not found:", input_file)
        continue

    # Convert audio to 16-bit PCM WAV, mono, 16000 Hz
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(input_file),
            "-ac", "1",
            "-ar", "16000",
            "-c:a", "pcm_s16le",
            str(converted_file)
        ],
        check=True
    )

    print("Audio converted successfully")

    # Read converted audio
    with open(converted_file, "rb") as file:
        audio_content = file.read()

    audio = speech.RecognitionAudio(content=audio_content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True
    )

    # Convert speech into text
    response = client.recognize(
        config=config,
        audio=audio,
        timeout=60
    )

    # Combine recognised text
    transcription = " ".join(
        result.alternatives[0].transcript
        for result in response.results
        if result.alternatives
    )

    # Save transcription
    transcription_file.write_text(transcription, encoding="utf-8")

    print("Transcription:", transcription)
    print("Saved to:", transcription_file)

print("\nFinished processing three recordings.")