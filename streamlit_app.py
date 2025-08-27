import streamlit as st
import modules.feature_engineer as feature_engineer
import modules.predictor as predictor
import modules.retriever as retriever
import modules.genai_agent as genai_agent
import modules.strategy_graph as strategy_graph

# --- App Config ---
st.set_page_config(page_title="StratoMind AI Assistant", layout="wide")
st.title(" StratoMind — AI Strategy Assistant")

# --- Sidebar Config ---
st.sidebar.header("Configuration")
domain = st.sidebar.selectbox("Domain", ["EdTech", "FinTech", "SaaS"])
query = st.sidebar.text_input("Ask StratoMind", placeholder="e.g., Growth strategy for B2B SaaS")

if st.sidebar.button("Run Analysis"):
    with st.spinner("Processing..."):
        docs = retriever.get_relevant_docs(domain, query)  # Stub
        features = feature_engineer.transform(query, domain)  # Stub
        pred, explanation = predictor.predict(features)  # Stub
        strategy = strategy_graph.run_strategy_pipeline(domain, query, docs, pred)  # Stub

    # Output
    st.subheader("📄 Suggested Strategy")
    st.write(strategy)

    st.subheader("📊 Prediction Insights")
    st.write(f"Prediction: {pred}")
    st.write(explanation)

st.info("Tip: Adjust domain and query to explore different strategies.")