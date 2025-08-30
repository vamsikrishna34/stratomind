from typing import Dict, Tuple, Callable, Any, Optional
import streamlit as st

# --- Fallback Prediction ---
def fallback_predict(features: Dict) -> Tuple[str, str]:
    """
    Fallback prediction logic when model is unavailable.

    Args:
        features (Dict): Feature dictionary from feature_engineer.py

    Returns:
        Tuple[str, str]: (Prediction label, Explanation string)
    """
    query_length = features.get("query_length", 0)
    keyword_hits = features.get("keyword_hits", 0)
    avg_steps = features.get("avg_steps", 0)

    score = query_length + (2 * keyword_hits) + avg_steps

    if score > 10:
        prediction = " High Growth Potential"
    elif score > 5:
        prediction = " Moderate Strategic Fit"
    else:
        prediction = "Low Strategic Alignment"

    explanation = (
        f"(Fallback Mode)\n"
        f"Prediction based on:\n"
        f" • Query length: {query_length}\n"
        f" • Keyword matches: {keyword_hits}\n"
        f" • Average step count: {avg_steps}\n\n"
        f"Weighted score = {score} → **{prediction}**"
    )

    return prediction, explanation

# --- Safe Call Wrapper ---
def safe_call(
    func: Callable,
    fallback_value: Any,
    *args,
    label: Optional[str] = None,
    show_error: bool = True,
    **kwargs
) -> Any:
    """
    Executes a function with error handling.
    Returns fallback_value if the function raises an exception.

    Args:
        func (Callable): Function to execute.
        fallback_value (Any): Value to return on failure.
        *args: Positional arguments for func.
        **kwargs: Keyword arguments for func.
        label (str, optional): Label for error context.
        show_error (bool): Whether to show Streamlit error banner.

    Returns:
        Any: Result of func or fallback_value.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        context = label or func.__name__
        msg = f"[Fallback] Error in {context}: {e}"
        print(msg)
        if show_error:
            st.warning(f"⚠️ {context} failed. Using fallback logic.")
        return fallback_value