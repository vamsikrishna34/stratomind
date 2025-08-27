import os
import pandas as pd
import streamlit as st
import modules.feature_engineer as feature_engineer
import modules.predictor as predictor
import modules.retriever as retriever
import modules.strategy_graph as strategy_graph
import modules.spark_etl as spark_etl   # fully integrated

# --- Page Config ---
st.set_page_config(page_title="StratoMind — AI Strategy Assistant", layout="wide")

# --- Inject Custom CSS if present ---
css_path = "assets/custom_styles.css"
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- App Header ---
st.title(" StratoMind — AI Strategy Assistant")
st.markdown("### Strategy, explained — powered by data and AI.")

# --- Sidebar Config ---
st.sidebar.header(" Configuration")
domain = st.sidebar.selectbox("Domain", ["EdTech", "FinTech", "SaaS"])
strategy_type = st.sidebar.text_input("Strategy Focus", placeholder="e.g., Content Strategy for B2B")

# --- File Upload ---
uploaded_file = st.sidebar.file_uploader(
    "📂 Upload CSV Data (optional)",
    type="csv",
    help="Provide your own dataset for a tailored analysis, or leave blank to use the built‑in sample."
)

# --- Main Logic Trigger ---
if st.sidebar.button(" Run Analysis"):
    with st.spinner(" Processing your strategy..."):
        # Step 1: Ingest data (uploaded or default)
        if uploaded_file is not None:
            docs = spark_etl.run_etl(uploaded_file)
            st.subheader(" Uploaded Data Preview")
            st.dataframe(docs.head(5), use_container_width=True)
        else:
            sample_path = "assets/sample_data.csv"
            if os.path.exists(sample_path):
                docs = spark_etl.run_etl(sample_path)
                st.subheader(" Sample Data Preview")
                st.dataframe(docs.head(5), use_container_width=True)
            else:
                st.error("No sample dataset found. Please upload a CSV to proceed.")
                st.stop()

        # Step 2: Feature engineering
        features = feature_engineer.transform(strategy_type, domain, docs)

        # Step 3: Predict outcomes
        pred, explanation = predictor.predict(features)

        # Step 4: Orchestrate final strategy
        strategy_output = strategy_graph.run_strategy_pipeline(domain, strategy_type, docs, pred)

    # --- Output Sections ---
    st.subheader(" Suggested Strategy")
    st.markdown(strategy_output)

    st.subheader(" Prediction Insights")
    st.markdown(f"**Prediction:** {pred}")
    st.write(explanation)

# --- Info Banner ---
st.info(
    "**How to use StratoMind**\n"
    "1. Pick a **domain** and enter your **strategy focus** in the sidebar.\n"
    "2. *(Optional)* Upload a CSV file for custom analysis.\n"
    "3. If you skip the upload, StratoMind will use its **sample dataset** so you can explore instantly.\n\n"
    "When ready, hit **Run Analysis** to generate your AI‑driven playbook."
)