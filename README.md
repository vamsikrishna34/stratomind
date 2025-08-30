# StratoMind: Modular AI Strategy Engine

StratoMind is a full-stack orchestration layer for AI strategy — built to ingest unstructured data, extract meaningful features, and deliver explainable, recruiter-facing insights. It combines GenAI, ML, and modular fallback logic to support scalable, narratable decision-making across domains.

---

## What It’s Used For

- **AI strategy prototyping**: Rapidly test and deploy explainable ML flows with GenAI enrichment  
- **Unstructured data ingestion**: Unified ETL pipeline for PDFs, DOCX, CSVs, and mixed-schema files  
- **Feature extraction & scoring**: Modular logic for keyword matching, complexity analysis, and skill inference  
- **Explainable predictions**: SHAP + XGBoost for transparent, demo-resilient outputs  
- **GenAI orchestration**: LangChain, LangGraph, and GPT4All integrations for agent-based workflows  
- **Recruiter-facing demos**: Toggleable UI, output cards, and info banners for polished walkthroughs  
- **Scalable backend**: Spark-ready architecture for enterprise-grade ingestion and transformation

---

##  Tech Stack

| Layer            | Tools & Libraries                             |
|------------------|-----------------------------------------------|
| UI               | Streamlit, YAML-configurable layout           |
| ML               | XGBoost, SHAP, scikit-learn                   |
| GenAI            | LangChain, LangGraph, GPT4All                 |
| File Parsing     | pdfplumber, python-docx                       |
| NLP              | TextBlob                                      |
| Big Data         | PySpark                                       |
| Config & Utils   | Modular YAML loader, fallback wrappers        |

---

##  Setup

### Docker (Recommended for demos)

```bash
# Clone the repo
git clone https://github.com/vamsikrishna34
cd stratomind

# Build and run
docker build -t stratodemo .
docker run -p 8501:8501 stratodemo