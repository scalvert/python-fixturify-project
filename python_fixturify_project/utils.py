from typing import Any, Dict, List, Union


def deep_merge(
    a: Dict[Any, Any], b: Dict[Any, Any], path: List[str] = []
) -> Dict[Any, Any]:
    """
    Merges dictionary b into dictionary a, with b overriding a for primitive values.

    Args:
        a (Dict[Any, Any]): The dictionary to merge into.
        b (Dict[Any, Any]): The dictionary to merge from.
        path (List[str], optional): The current path in the dictionary. Defaults to [].

    Returns:
        Dict[Any, Any]: The merged dictionary.

    Raises:
        Exception: If there is a conflict between the values being merged.

    """
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                deep_merge(a[key], b[key], path + [str(key)])
            elif isinstance(a[key], (int, float, str, bool)) and isinstance(
                b[key], (int, float, str, bool)
            ):
                a[key] = b[key]
            else:
                raise Exception("Conflict at %s" % ".".join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def keys_exists(element: Dict[Any, Any], *keys: Union[str, int]) -> bool:
    """
    Check if the specified nested keys exist in the given dictionary.

    Args:
        element (Dict[Any, Any]): The dictionary to check.
        *keys (Union[str, int]): The nested keys to check for.

    Returns:
        bool: True if all keys exist, False otherwise.

    Raises:
        AttributeError: If the first argument is not a dictionary.
        AttributeError: If less than two arguments are provided.

    """
    if not isinstance(element, dict):
        raise AttributeError("keys_exists() expects dict as first argument.")
    if len(keys) == 0:
        raise AttributeError("keys_exists() expects at least two arguments, one given.")

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True
