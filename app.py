import logging
import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from services.core import run_pronunciation_scoring

load_dotenv()


def configure_logging() -> logging.Logger:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    root_logger = logging.getLogger()

    if not root_logger.handlers:
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        )
    else:
        root_logger.setLevel(level)

    return logging.getLogger("pronounceright.app")


logger = configure_logging()

st.set_page_config(page_title="PronounceRight", page_icon="🚀", layout="wide")
st.title("PronounceRight")
st.caption("Word-level pronunciation scoring with confidence-weighted alignment and coaching tips.")

target_sentence = st.text_input("Target Sentence", value="I am excited to build reliable AI products.")
spoken_transcript = st.text_area("Spoken Transcript", height=120, value="I am excited to build reliable AI product")
confidence_input = st.text_input("Optional confidences (comma-separated, 0 to 1)", value="0.9,0.88,0.9,0.82,0.7,0.8,0.76,0.65")

if st.button("Score Pronunciation", type="primary"):
    logger.info("Button clicked for PronounceRight")
    output = run_pronunciation_scoring(target_sentence, spoken_transcript, confidence_input)

    if output.get("error"):
        st.error(output["error"])
        st.stop()

    st.success("Scoring completed")
    st.metric("Pronunciation Score", output["pronunciation_score"])

    df = pd.DataFrame(output["word_results"])
    st.subheader("Word-Level Results")
    st.dataframe(df, use_container_width=True)

    st.subheader("Coaching Tips")
    for tip in output["coaching_tips"]:
        st.write("- " + tip)
