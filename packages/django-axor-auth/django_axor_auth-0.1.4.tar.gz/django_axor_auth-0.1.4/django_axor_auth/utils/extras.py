from typing import Any


def get_if_present(data: dict[str, Any], key: str, default: Any = None) -> Any:
    if key in data:
        return data[key]
    return default
