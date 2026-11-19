# Human Voice Detection: Human or AI?

A mobile application that analyses voice recordings to estimate whether the speaker is a real human or an AI-generated voice.

## About

Scam Sheild is a mobile application that analyses voice recordings to estimate whether the speaker is a real human or an AI-generated voice.

This project was completed as part of our Agile Process module to learn how Agile project management works in practice.

## Problem

***"Make sure that it is a human behind the phone and not a bot."***

This project aims to create a barrier between potential cybercriminals and the person receiving the call by analysing voice recordings and identifying whether the speaker is likely to be human or AI-generated. 

## Features

- Upload a voice recording for analysis
- Classify audio as **likely human**, **likely AI-generated**, or **inconclusive**
- Display a confidence score
- Compare machine-learning models
- Evaluate performance on noisy, compressed, and short audio
- Mobile user accounts, scam-call log, and admin dashboard

## How it Works

1. The user uploads an audio recording.
2. The app preprocesses the audio and extracts features.
3. The selected machine-learning model classifies the recording.
4. The app displays the result and confidence score.

The result is an estimate, not proof that a call is a scam.

## Machine Learning 
The project compares:

- **1** — uses 
- **2** — uses 

Both models are evaluated using accuracy, precision, recall, F1-score, and confusion matrices. The best-performing model is integrated into the mobile app.

## Dataset

The dataset contains genuine human speech and AI-generated voice recordings. Each recording includes its source, licence, consent status, speaker label, collection date, and class label.

## Usage

```bash
# ...
```

## Team

- Rebecca — Product Owner, Scrum Master (Sprint 3) and Developer
- Cassandra — Scrum Master (Sprint 1) and Developer
- Ibrahim — Scrum Master (Sprint 2) and Developer
