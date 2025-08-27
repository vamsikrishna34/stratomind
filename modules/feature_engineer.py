from typing import List, Dict
import numpy as np

def transform(strategy_query: str, domain: str, strategy_docs: List[Dict]) -> Dict:
    """
    Transforms strategy input into a feature dictionary.

    Args:
        strategy_query (str): User-entered strategy prompt.
        domain (str): Selected domain (e.g., 'EdTech').
        strategy_docs (List[Dict]): Retrieved strategy data.

    Returns:
        Dict: Feature dictionary for prediction.
    """
    # Basic keyword features
    query_len = len(strategy_query.split())
    keyword_hits = sum([
        strategy_query.lower() in s["title"].lower() or strategy_query.lower() in s["description"].lower()
        for s in strategy_docs
    ])

    # Strategy complexity features
    avg_steps = np.mean([len(s.get("steps", [])) for s in strategy_docs]) if strategy_docs else 0

    # Domain encoding (stub — replace with one-hot or embedding later)
    domain_map = {"EdTech": 0, "FinTech": 1, "SaaS": 2}
    domain_encoded = domain_map.get(domain, -1)

    return {
        "query_length": query_len,
        "keyword_hits": keyword_hits,
        "avg_steps": avg_steps,
        "domain_encoded": domain_encoded,
        "raw_query": strategy_query,
        "raw_domain": domain
    }