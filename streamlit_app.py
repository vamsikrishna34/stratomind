import os
import pandas as pd
import streamlit as st
import modules.feature_engineer as feature_engineer
import modules.predictor as predictor
import modules.retriever as retriever
import modules.strategy_graph as strategy_graph
# If you have a Spark ETL module, import it here:
# import modules.spark_etl as spark_etl

# --- Page Config ---
st.set_page_config(page_title="StratoMind AI Assistant", layout="wide")

# --- Inject Custom CSS if present ---
css_path = "assets/custom_styles.css"
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- App Header ---
st.title("StratoMind — AI Strategy Assistant")
st.markdown("### Strategy, explained.")

# --- Sidebar Config ---
st.sidebar.header("Configuration")
domain = st.sidebar.selectbox("Domain", ["EdTech", "FinTech", "SaaS"])
strategy_type = st.sidebar.text_input("Strategy", placeholder="e.g., Content Strategy for B2B")

# --- File Upload ---
uploaded_file = st.sidebar.file_uploader("Upload CSV Data", type="csv")

# --- Main Logic Trigger ---
if st.sidebar.button("Run Analysis"):
    with st.spinner("Processing..."):
        if uploaded_file is not None:
            # User provided a CSV → load into DataFrame
            df = pd.read_csv(uploaded_file)
            # Option A: Pass raw DF directly to feature engineering
            docs = df
            # Option B (if using Spark ETL): docs = spark_etl.run_etl(df)
        else:
            # Fall back to default retriever pipeline
            docs = retriever.get_relevant_docs(domain, strategy_type)

        # Step 2: Feature engineering
        features = feature_engineer.transform(strategy_type, domain, docs)

        # Step 3: Predict outcomes
        pred, explanation = predictor.predict(features)

        # Step 4: Orchestrate final strategy
        strategy_output = strategy_graph.run_strategy_pipeline(domain, strategy_type, docs, pred)

    # --- Output Sections ---
    st.subheader("Suggested Strategy")
    st.markdown(strategy_output)

    st.subheader("Prediction Insights")
    st.markdown(f"**Prediction:** {pred}")
    st.write(explanation)

# --- Info Banner ---
st.info("Tip: Adjust domain, strategy, or upload a CSV to explore different contexts.")