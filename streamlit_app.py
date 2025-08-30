import os
import pandas as pd
import streamlit as st
import pdfplumber
from docx import Document

import modules.feature_engineer as feature_engineer
import modules.predictor as predictor
from modules.fallback import fallback_predict
import modules.retriever as retriever
import modules.strategy_graph as strategy_graph
import modules.spark_etl as spark_etl

# --- Page Config ---
st.set_page_config(page_title="StratoMind — AI Strategy Assistant", layout="wide")

# --- Inject Custom CSS ---
css_path = "assets/custom_styles.css"
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Helpers for parsing all file types into DataFrame ---
def parse_uploaded_file(file):
    name = file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file)
    elif name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            text = "\n".join([p.extract_text() or "" for p in pdf.pages])
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return pd.DataFrame({"content": lines})
    elif name.endswith(".docx"):
        doc = Document(file)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return pd.DataFrame({"content": lines})
    else:
        return None

# --- App Header ---
st.markdown("<h1 class='section-header'> StratoMind</h1>", unsafe_allow_html=True)
st.markdown("#### Your AI‑powered strategy co‑pilot — from raw data to explainable playbooks.")

# --- Sidebar: Control Panel ---
st.sidebar.markdown("##  Configuration")
domain = st.sidebar.selectbox("🗂 Select Domain", ["EdTech", "FinTech", "SaaS"])
strategy_type = st.sidebar.text_input(" Strategy Focus", placeholder="e.g., Customer Strategy: B2B")
uploaded_file = st.sidebar.file_uploader("📂 Upload CSV, PDF, or Word (optional)", type=["csv", "pdf", "docx"])
run_button = st.sidebar.button(" Run Analysis")

# --- Main Panel ---
if run_button:
    with st.spinner("🔍 Analyzing your strategy..."):
        # Step 1: File ingestion
        if uploaded_file:
            df = parse_uploaded_file(uploaded_file)
            if df is None or df.empty:
                st.error("Unsupported or empty file. Please upload a valid CSV, PDF, or DOCX.")
                st.stop()
            docs = spark_etl.run_etl(df)
            st.markdown("<h4 class='section-header'>📄 Uploaded File Preview</h4>", unsafe_allow_html=True)
            st.dataframe(docs.head(5), use_container_width=True)
        else:
            sample_path = "assets/sample_data.csv"
            if os.path.exists(sample_path):
                docs = spark_etl.run_etl(sample_path)
                st.markdown("<h4 class='section-header'>📄 Sample Data Preview</h4>", unsafe_allow_html=True)
                st.dataframe(docs.head(5), use_container_width=True)
            else:
                st.error("No sample dataset found. Please upload a file.")
                st.stop()

        # Step 2: Feature engineering
        features = feature_engineer.transform(strategy_type, domain, docs)

        # Step 3: Prediction with fallback
        try:
            if predictor.model is not None:
                pred, explanation = predictor.predict(features)
            else:
                raise RuntimeError("Model not loaded")
        except Exception as e:
            st.warning(f"⚠️ Model error: {e}. Using fallback logic.")
            pred, explanation = fallback_predict(features)

        # Step 4: Strategy generation
        try:
            strategy_output = strategy_graph.run_strategy_pipeline(domain, strategy_type, docs, pred)
        except Exception as e:
            strategy_output = f"⚠️ Strategy generation failed: {e}"

    # --- Output Cards ---
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h4 class='section-header'>🧩 Suggested Strategy</h4>", unsafe_allow_html=True)
    st.markdown(strategy_output)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h4 class='section-header'>📊 Prediction Insights</h4>", unsafe_allow_html=True)
    st.markdown(f"**Prediction:** {pred}")
    st.markdown(explanation)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- Hero Section Before Analysis ---
    hero_col1, hero_col2 = st.columns([1.2, 0.8])

    with hero_col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h4 class='section-header'>🛠️ How to use StratoMind</h4>", unsafe_allow_html=True)
        st.markdown(
            "1️⃣ Pick a **domain** and enter your **strategy focus** in the sidebar.\n"
            "2️⃣ *(Optional)* Upload a CSV, PDF, or Word document for a custom analysis.\n"
            "3️⃣ Skip the upload to use the **sample dataset**.\n\n"
            "▶️ When ready, hit **Run Analysis** to get your AI‑driven playbook."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with hero_col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### ✨ What you'll get")
        st.markdown(
            "- A tailored, data‑driven strategy\n"
            "- Predictive insights with context\n"
            "- Transparent reasoning for each suggestion"
        )
        st.markdown("</div>", unsafe_allow_html=True)