# Scam Shield - Agile Processes
# Google Cloud Speech-to-Text
# Transcribe remaining human voice recordings

from pathlib import Path
import subprocess

from google.cloud import speech


# Step 1: Configure input and output folders

input_folder = Path("dataset/raw/Human")
output_folder = Path("dataset/processed")

output_folder.mkdir(parents=True, exist_ok=True)


# Step 2: Create Google Cloud Speech-to-Text client

client = speech.SpeechClient()


# Step 3: Find available audio recordings

audio_files = sorted(input_folder.glob("*.wav"))

print("Total available recordings:", len(audio_files))


# Step 4: Process up to five new recordings

MAX_FILES = 22

processed = 0
skipped = 0
failed = 0

for audio_file in audio_files:

    if processed >= MAX_FILES:
        break

    filename = audio_file.stem

    transcription_file = output_folder / f"{filename}_transcription.txt"
    converted_file = output_folder / f"{filename}_converted.wav"

    # Skip recordings that already have transcriptions
    if transcription_file.exists():
        print("Skipping already transcribed:", audio_file.name)
        skipped += 1
        continue

    print("\nProcessing:", audio_file.name)

    try:
        # Convert audio into 16 kHz, mono, 16-bit PCM
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(audio_file),
                "-ar",
                "16000",
                "-ac",
                "1",
                "-c:a",
                "pcm_s16le",
                str(converted_file)
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Read converted audio
        audio_content = converted_file.read_bytes()

        audio = speech.RecognitionAudio(content=audio_content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US"
        )

        # Send audio to Google Cloud Speech-to-Text
        response = client.recognize(
            config=config,
            audio=audio
        )

        # Combine recognised sentences
        transcript = "\n".join(
            result.alternatives[0].transcript
            for result in response.results
            if result.alternatives
        )

        # Save transcription
        transcription_file.write_text(
            transcript,
            encoding="utf-8"
        )

        processed += 1

        print("SUCCESS:", transcription_file)

    except Exception as error:

        failed += 1
        print("ERROR:", audio_file.name, error)


# Step 5: Print final summary

print("\nSCRUM: Speech-to-Text Processing Summary")
print("New recordings transcribed:", processed)
print("Already transcribed:", skipped)
print("Failed:", failed)