import importlib
from typing import List, Dict

def get_relevant_docs(domain: str, strategy: str = "") -> List[Dict]:
    """
    Retrieves structured strategy data for the given domain.

    Args:
        domain (str): Domain name (e.g., 'EdTech', 'FinTech', 'SaaS').
        strategy (str): Optional search term to filter strategies.

    Returns:
        List[Dict]: Matching strategies as a list of dicts.
    """
    try:
        module_name = f"assets.strategy_docs.{domain.lower()}_strategies"
        strategies = importlib.import_module(module_name).STRATEGIES

        # Filter if a search term is provided
        if strategy:
            filtered = [
                s for s in strategies
                if strategy.lower() in s["title"].lower()
                or strategy.lower() in s["description"].lower()
            ]
            return filtered if filtered else strategies

        return strategies

    except ModuleNotFoundError:
        return [{
            "title": "N/A",
            "description": f"No strategies found for {domain}",
            "steps": []
        }]