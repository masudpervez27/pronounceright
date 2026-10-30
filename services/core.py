import logging
import difflib
import re

logger = logging.getLogger(__name__)


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z']+", text.lower())


def _parse_confidences(raw: str) -> list[float]:
    if not raw.strip():
        return []
    vals: list[float] = []
    for piece in re.split(r"[,\s]+", raw.strip()):
        if not piece:
            continue
        try:
            val = float(piece)
        except ValueError:
            continue
        vals.append(max(0.0, min(1.0, val)))
    return vals


def _align_words(target_words: list[str], spoken_words: list[str]) -> list[tuple[str, str, str, int | None]]:
    # Returns tuples: (expected, actual, status, spoken_index)
    matcher = difflib.SequenceMatcher(a=target_words, b=spoken_words)
    alignment: list[tuple[str, str, str, int | None]] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for offset in range(i2 - i1):
                alignment.append((target_words[i1 + offset], spoken_words[j1 + offset], "correct", j1 + offset))
        elif tag == "replace":
            length = max(i2 - i1, j2 - j1)
            for offset in range(length):
                expected = target_words[i1 + offset] if i1 + offset < i2 else ""
                actual = spoken_words[j1 + offset] if j1 + offset < j2 else ""
                spoken_index = j1 + offset if j1 + offset < j2 else None
                if expected:
                    alignment.append((expected, actual, "substituted", spoken_index))
        elif tag == "delete":
            for offset in range(i2 - i1):
                alignment.append((target_words[i1 + offset], "", "missed", None))
        elif tag == "insert":
            # extra spoken words are not penalized directly
            continue

    return alignment


def _coaching_tips(rows: list[dict]) -> list[str]:
    missed = [r["expected"] for r in rows if r["status"] == "missed"]
    low_conf = [r["expected"] for r in rows if r["confidence"] < 0.55]

    tips: list[str] = []
    if missed:
        tips.append("Practice missing words slowly first: " + ", ".join(missed[:6]))
    if low_conf:
        tips.append("Repeat low-confidence words in short phrases: " + ", ".join(low_conf[:6]))
    if not tips:
        tips.append("Strong attempt. Increase pace gradually while keeping pronunciation clarity.")
    return tips


def run_pronunciation_scoring(target_sentence: str, spoken_transcript: str, confidence_input: str = "") -> dict:
    logger.info(
        "Processing pronunciation scoring (target_chars=%d, transcript_chars=%d)",
        len(target_sentence),
        len(spoken_transcript),
    )
    if not target_sentence.strip() or not spoken_transcript.strip():
        logger.warning("Empty input received")
        return {"error": "Please provide both target sentence and spoken transcript."}

    target_words = _tokenize(target_sentence)
    spoken_words = _tokenize(spoken_transcript)

    if not target_words:
        return {"error": "Target sentence has no valid words to score."}

    confidences = _parse_confidences(confidence_input)
    if len(confidences) < len(spoken_words):
        confidences.extend([0.75] * (len(spoken_words) - len(confidences)))

    alignment = _align_words(target_words, spoken_words)

    rows: list[dict] = []
    weighted_total = 0.0
    for expected, actual, status, spoken_idx in alignment:
        conf = confidences[spoken_idx] if spoken_idx is not None and spoken_idx < len(confidences) else 0.5
        if status == "correct":
            word_score = 1.0 * conf
        elif status == "substituted":
            word_score = 0.4 * conf
        else:
            word_score = 0.0

        weighted_total += word_score
        rows.append(
            {
                "expected": expected,
                "actual": actual,
                "status": status,
                "confidence": round(conf, 2),
                "word_score": round(word_score, 2),
            }
        )

    pronunciation_score = int(round((weighted_total / max(1, len(target_words))) * 100))
    pronunciation_score = max(0, min(100, pronunciation_score))

    tips = _coaching_tips(rows)

    logger.info("Pronunciation scoring completed with score=%d for %d target words", pronunciation_score, len(target_words))

    return {
        "target_sentence": target_sentence,
        "spoken_transcript": spoken_transcript,
        "pronunciation_score": pronunciation_score,
        "word_results": rows,
        "coaching_tips": tips,
    }
