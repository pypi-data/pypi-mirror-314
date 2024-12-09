from functools import wraps
from typing import Any, Callable


def convert_booleans_to_strings(func: Callable) -> Callable:
    """
    Decorador para transformar valores booleanos en cadenas "true" o "false".
    """

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict[str, Any]) -> Any:
        data = func(*args, **kwargs)
        if isinstance(data, dict):
            return transform_bools(data)
        return data

    return wrapper


def transform_bools(data: Any) -> Any:
    """
    Transforma recursivamente los valores booleanos en "true" o "false".
    """
    if isinstance(data, dict):
        return {k: transform_bools(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [transform_bools(item) for item in data]
    elif isinstance(data, bool):
        return "true" if data else "false"
    return data
