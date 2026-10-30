# PronounceRight - YouTube Transcript Script

## Title
Build a Pronunciation Scorer with Word Alignment and Coaching Tips (Project 12)

## Intro
This project implements PronounceRight from the portfolio plan.

We compare:
- target sentence,
- spoken transcript,
- optional confidence scores.

Then we produce:
- pronunciation score,
- word-level diagnostics,
- personalized coaching tips.

## Scoring logic
1. Tokenize both target and spoken text.
2. Align words with sequence matching.
3. Label each target word as correct, substituted, or missed.
4. Apply confidence-weighted scoring per word.
5. Aggregate to a 0-100 pronunciation score.

## UI
The Streamlit app collects target sentence, transcript, and optional confidences.

It displays:
- overall pronunciation score,
- word-level result table,
- coaching recommendations.

## Logging
The pipeline logs start and completion with safe metadata and total score.

## Outro
This creates a measurable pronunciation workflow and can later be connected to real STT confidence outputs.
