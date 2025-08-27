from typing import Callable, Any

def safe_call(func: Callable, fallback_value: Any, *args, **kwargs) -> Any:
    """
    Executes a function with error handling.
    Returns fallback_value if the function raises an exception.

    Args:
        func (Callable): Function to execute.
        fallback_value (Any): Value to return on failure.
        *args: Positional arguments for func.
        **kwargs: Keyword arguments for func.

    Returns:
        Any: Result of func or fallback_value.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"[Fallback] Error in {func.__name__}: {e}")
        return fallback_value