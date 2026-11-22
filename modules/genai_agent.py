from typing import List, Dict
from langchain.tools import Tool

def format_strategy(doc: Dict) -> str:
    """
    Formats a single strategy document into a readable narrative block.
    """
    title = doc.get("title", "Untitled Strategy")
    description = doc.get("description", "No description provided.")
    steps = doc.get("steps", [])

    lines = [f"🔹 **{title}** — {description}"]
    if steps and isinstance(steps, list):
        for i, step in enumerate(steps, 1):
            if isinstance(step, str) and step.strip():
                lines.append(f"  {i}. {step.strip()}")
            else:
                lines.append(f"  {i}. [Missing step description]")
    else:
        lines.append("  No actionable steps provided.")

    return "\n".join(lines)

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
        return f" No relevant strategies found for '{query}'. Try refining your prompt or uploading more context."

    header = f" Strategic Overview for: **{query}**\n\n" if query else " Strategic Overview:\n\n"
    body = "\n\n".join([format_strategy(doc) for doc in strategy_docs])
    return header + body

# LangChain Tool wrapper
generate_strategy_tool = Tool.from_function(
    name="generate_strategy",
    description="Generates a strategic narrative from structured strategy documents and a user query.",
    func=lambda inputs: generate_strategy(inputs.get("strategy_docs", []), inputs.get("query", "")),
    args_schema=None  # Optional: define Pydantic schema for stricter input validation
)