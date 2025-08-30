from typing import List, Dict, Any, Union
import numpy as np
import pandas as pd

def transform(strategy_query: Any, domain: str, strategy_docs: Union[List[Dict], pd.DataFrame]) -> Dict:
    """
    Transforms strategy input into a feature dictionary.

    Args:
        strategy_query (str | Any): User-entered strategy prompt. Will be coerced to str.
        domain (str): Selected domain (e.g., 'EdTech').
        strategy_docs (List[Dict] | pd.DataFrame): Retrieved strategy data.

    Returns:
        Dict: Feature dictionary for prediction.
    """
    # --- Normalize and sanitize inputs ---
    query_str = str(strategy_query or "").strip()
    query_lower = query_str.lower()

    # Defensive fallback for empty or invalid input
    if isinstance(strategy_docs, pd.DataFrame):
        safe_docs = strategy_docs.to_dict(orient="records") if not strategy_docs.empty else []
    elif isinstance(strategy_docs, list):
        safe_docs = strategy_docs if strategy_docs else []
    else:
        safe_docs = []

    # Basic keyword features
    query_len = len(query_str.split())

    keyword_hits = sum(
        query_lower in str(s.get("title", "")).lower() or
        query_lower in str(s.get("description", "")).lower()
        for s in safe_docs
    )

    # Strategy complexity features
    avg_steps = np.mean([
        len(s.get("steps", [])) if isinstance(s.get("steps", []), (list, tuple)) else 0
        for s in safe_docs
    ]) if safe_docs else 0

    # --- One-hot domain encoding ---
    domain_keys = ["EdTech", "FinTech", "SaaS"]
    domain_onehot = {f"domain_{key}": int(domain == key) for key in domain_keys}

    return {
        "query_length": query_len,
        "keyword_hits": keyword_hits,
        "avg_steps": avg_steps,
        **domain_onehot,
        "raw_query": query_str,
        "raw_domain": domain
    }