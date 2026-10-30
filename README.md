# PronounceRight

Pronunciation scoring starter app with logging-enabled feedback generation.

## What It Does

- Compares target sentence words against spoken transcript words
- Uses confidence-weighted token alignment for scoring
- Outputs word-level diagnostics (correct/substituted/missed)
- Generates focused coaching tips from weak pronunciations

## Implemented Feature Slice

- Token-level alignment between target sentence and spoken transcript
- Confidence-weighted pronunciation scoring (0-100)
- Word-level diagnostics: correct/substituted/missed
- Actionable coaching tips based on weak words and misses
- Streamlit table output for detailed feedback

## Architecture

```mermaid
flowchart TD
    subgraph Input["📥 Inputs"]
        A[Target sentence] --> B[Tokenizer]
        C[Spoken transcript] --> D[Tokenizer]
        E[Confidence values] --> F[Confidence parser]
    end

    subgraph Scoring["🗣️ Pronunciation Scoring"]
        G[Sequence alignment\nengine] --> H[Word status\nclassifier]
        H --> I[Confidence-weighted\nscorer]
        I --> J[Coaching tip\ngenerator]
    end

    subgraph UI["🖥️ Streamlit"]
        K[Score +\ndiagnostics table]
    end

    B --> G
    D --> G
    F --> I
    J --> K

    classDef source fill:#1e40af,stroke:#93c5fd,stroke-width:2px,color:#ffffff
    classDef process fill:#0f766e,stroke:#5eead4,stroke-width:2px,color:#ffffff
    classDef rank fill:#6d28d9,stroke:#c4b5fd,stroke-width:2px,color:#ffffff
    classDef llm fill:#b91c1c,stroke:#fca5a5,stroke-width:2px,color:#ffffff
    classDef ui fill:#15803d,stroke:#86efac,stroke-width:2px,color:#ffffff

    class A,C,E source
    class B,D,F,G process
    class H,I rank
    class J llm
    class K ui

    style Input fill:#f1f5f9,stroke:#334155,stroke-width:2px,color:#0f172a
    style Scoring fill:#f1f5f9,stroke:#334155,stroke-width:2px,color:#0f172a
    style UI fill:#f1f5f9,stroke:#334155,stroke-width:2px,color:#0f172a

    linkStyle default stroke:#f59e0b,stroke-width:2px
```

## Outcome

- Produces objective pronunciation feedback at word level
- Makes practice measurable with a repeatable score
- Guides learners with actionable, targeted pronunciation advice

## Quick Start

### Prerequisites

- [UV](https://docs.astral.sh/uv/) installed (`powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` on Windows)

### Run Locally

```bash
cd pronounceright
uv sync

uv run streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

```
pronounceright/
├── app.py                  # Streamlit entry point — target, transcript, confidence inputs + score + table + tips
├── services/
│   ├── __init__.py
│   └── core.py             # Tokenizer, alignment engine, word classifier, scorer, tip generator
├── .streamlit/
│   └── config.toml         # App theme
├── pyproject.toml          # UV dependencies
└── README.md
```

---

## Logging

- Logging is configured on startup.
- Use LOG_LEVEL to adjust verbosity.
