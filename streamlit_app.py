import streamlit as st
import modules.feature_engineer as feature_engineer
import modules.predictor as predictor
import modules.retriever as retriever
import modules.genai_agent as genai_agent
import modules.strategy_graph as strategy_graph

# --- App Config ---
st.set_page_config(page_title="StratoMind AI Assistant", layout="wide")
st.title("StratoMind — AI Strategy Assistant")
st.markdown("### Strategy, explained.")

# --- Sidebar Config ---
st.sidebar.header("Configuration")
domain = st.sidebar.selectbox("Domain", ["EdTech", "FinTech", "SaaS"])
strategy_type = st.sidebar.text_input("Strategy", placeholder="e.g., Content Strategy for B2B")

if st.sidebar.button("Run Analysis"):
    with st.spinner("Processing..."):
        # Step 1: Get relevant docs
        docs = retriever.get_relevant_docs(domain, strategy_type)

        # Step 2: Feature engineering
        features = feature_engineer.transform(strategy_type, domain)

        # Step 3: Predict outcomes
        pred, explanation = predictor.predict(features)

        # Step 4: Run multi-agent reasoning
        strategy = strategy_graph.run_strategy_pipeline(domain, strategy_type, docs, pred)

    st.subheader("Suggested Strategy")
    st.write(strategy)

    st.subheader(" Prediction Insights")
    st.write(f"Prediction: {pred}")
    st.write(explanation)

st.info("Tip: Adjust domain and strategy to explore different contexts.")