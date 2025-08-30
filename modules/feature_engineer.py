from typing import List, Dict, Any
import numpy as np

def transform(strategy_query: Any, domain: str, strategy_docs: List[Dict]) -> Dict:
    """
    Transforms strategy input into a feature dictionary.

    Args:
        strategy_query (str | Any): User-entered strategy prompt. Will be coerced to str.
        domain (str): Selected domain (e.g., 'EdTech').
        strategy_docs (List[Dict]): Retrieved strategy data.

    Returns:
        Dict: Feature dictionary for prediction.
    """
    # --- Normalize and sanitize inputs ---
    query_str = str(strategy_query or "").strip()
    query_lower = query_str.lower()

    safe_docs = strategy_docs or []

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