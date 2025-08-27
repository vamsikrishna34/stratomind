def safe_call(func, fallback_value, *args, **kwargs):
    """
    Executes a function with error handling — returns fallback_value on failure.
    """
    try:
        return func(*args, **kwargs)
    except Exception:
        return fallback_value