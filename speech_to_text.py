# Google Cloud Speech-to-Text
# Agile Processes - Scam Shield Project
# Convert a WAV audio recording into text

from google.cloud import speech
from pathlib import Path

# Locate the audio recording
audio_file = Path("dataset/processed/1210_converted.wav")
# Create the Speech-to-Text client
client = speech.SpeechClient()

# Read the audio file
with open(audio_file, "rb") as file:
    audio_content = file.read()

# Configure the audio
audio = speech.RecognitionAudio(content=audio_content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US"
)

# Send audio to Google Cloud
print("Converting audio to text...")

response = client.recognize(
    config=config,
    audio=audio
)

# Display and save transcription
transcriptions = []

for result in response.results:
    transcript = result.alternatives[0].transcript
    transcriptions.append(transcript)
    print("Transcription:", transcript)

output_file = Path("dataset/processed/test_transcription.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

output_file.write_text(
    "\n".join(transcriptions),
    encoding="utf-8"
)

print("Transcription saved to:", output_file)