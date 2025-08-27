from typing import List, Dict

def generate_strategy(strategy_docs: List[Dict], query: str) -> str:
    """
    Generates a strategic narrative based on retrieved docs and user query.

    Args:
        strategy_docs (List[Dict]): Structured strategy data.
        query (str): User-entered strategy prompt.

    Returns:
        str: Generated strategy narrative.
    """
    if not strategy_docs:
        return f"No relevant strategies found for '{query}'. Try refining your prompt."

    # Stub logic — will be replaced by LangChain agent
    summary_lines = []
    for doc in strategy_docs:
        title = doc.get("title", "Untitled")
        desc = doc.get("description", "")
        steps = doc.get("steps", [])
        summary_lines.append(f"🔹 **{title}** — {desc}")
        for i, step in enumerate(steps, 1):
            summary_lines.append(f"  {i}. {step}")

    return "\n".join(summary_lines)