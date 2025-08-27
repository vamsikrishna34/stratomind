from typing import List, Dict
import modules.genai_agent as genai_agent

def run_strategy_pipeline(domain: str, query: str, strategy_docs: List[Dict], prediction: str) -> str:
    """
    Orchestrates strategy generation using multi-agent logic.

    Args:
        domain (str): Selected domain (e.g., 'EdTech').
        query (str): User-entered strategy prompt.
        strategy_docs (List[Dict]): Retrieved strategy data.
        prediction (str): Prediction label from predictor.py

    Returns:
        str: Final strategy narrative.
    """
    # Step 1: Generate base strategy from docs
    base_strategy = genai_agent.generate_strategy(strategy_docs, query)

    # Step 2: Add prediction context
    final_output = (
        f"### Strategy Summary for '{query}' in {domain}\n\n"
        f"**Predicted Outcome:** {prediction}\n\n"
        f"{base_strategy}"
    )

    return final_output