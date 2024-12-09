"""
JSON Parse Utils
"""
from typing import Any


def get_single_value_by_key(json_obj: dict, target_key: str) -> Any:
    """
    Get the first value by key from JSON object.
    Input:
    - json_obj: dict, the JSON object.
    - target_key: str, the target key.
    Output:
    - Any: The value for that key.
    """
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key == target_key:
                return value
            elif isinstance(value, (dict, list)):
                result = get_single_value_by_key(value, target_key)
                if result is not None:
                    return result
    elif isinstance(json_obj, list):
        for item in json_obj:
            result = get_single_value_by_key(item, target_key)
            if result is not None:
                return result
    return None


def get_multi_values_by_key(json_obj: dict, target_key: str) -> list[Any]:
    """
    Get all values by key from JSON object.
    Input:
    - json_obj: dict, the JSON object.
    - target_key: str, the target key.
    Output:
    - list[Any]: The values for that key.
    """
    results = []

    def recursive_search(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == target_key:
                    results.append(value)
                elif isinstance(value, (dict, list)):
                    recursive_search(value)
        elif isinstance(obj, list):
            for item in obj:
                recursive_search(item)

    recursive_search(json_obj)

    return results


def find_first_nested_dict(data, key: str, value: Any):
    """
    Find the first nested dict
    Input:
    - data: dict, the JSON object.
    - key: str, the target key.
    - value: Any, the target value.
    Output:
    - Any: The value for that key.
    """
    if isinstance(data, dict):
        if key in data and data[key] == value:
            return data
        for v in data.values():
            result = find_first_nested_dict(v, key, value)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_first_nested_dict(item, key, value)
            if result is not None:
                return result
    return None


def find_all_nested_dicts(data, key, value):
    """
    Find all nested dicts
    Input:
    - data: dict, the JSON object.
    - key: str, the target key.
    - value: Any, the target value.
    Output:
    - list[Any]: The values for that key.
    """
    result = []
    if isinstance(data, dict):
        if key in data and data[key] == value:
            result.append(data)
        for v in data.values():
            result.extend(find_all_nested_dicts(v, key, value))
    elif isinstance(data, list):
        for item in data:
            result.extend(find_all_nested_dicts(item, key, value))
    return result
