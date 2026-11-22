# Project memory

## Product intent & audience

- "StratoMind" is a Streamlit app deployed on Streamlit Cloud.
- Likely a strategy-generation / decision-support tool (modules: `strategy_graph`, `genai_agent`).
- Entry point: `streamlit_app.py` at repo root.

## Brand personality & voice

- Not yet inferred; default to clear, technical, fix-oriented explanations.

## Visual design & UX direction

- Streamlit-based UI; no custom design tokens inferred yet.
- App must load even when optional AI dependencies (langchain) are missing.

## Decisions, constraints & rationale

- Architecture: `streamlit_app.py` → `modules/strategy_graph.py` → `modules/genai_agent.py`.
- `genai_agent.generate_strategy` is the core logic and must not require langchain.
- LangChain `Tool` wrapper is optional; only created when langchain is importable.
- Rationale: top-level `from langchain.tools import Tool` crashed the entire app on Streamlit Cloud when langchain wasn't installed or the import path changed. Making it optional prevents total app failure and decouples core strategy logic from the agent-tooling layer.
- Pattern: prefer optional/conditional imports for heavy or version-sensitive AI deps; keep core logic dependency-light.
- pandas may be a runtime dependency (sandbox showed missing-dep noise, not the real bug).

## Open questions & assumptions

- Which langchain version is intended, and is `Tool` still at `langchain.tools`? (Path may need updating if langchain is later installed.)
- Is langchain/langgraph expected in production on Streamlit Cloud, or intentionally omitted?
- Should the LangChain `Tool` wrapper live in a separate module from core `generate_strategy` for cleaner separation?
- Are there other top-level langchain/langgraph imports elsewhere that could fail similarly? (Verified this turn: `strategy_graph` only needs `generate_strategy`.)
- Streamlit Cloud dependency manifest (requirements.txt) contents not yet confirmed.