from typing import Any, Dict, List, Tuple, Union

def deep_merge(a: Dict[Any, Any], b: Dict[Any, Any], path: List[str] = []) -> Dict[Any, Any]:
    """
    Merges dictionary b into dictionary a, with b overriding a for primitive values.
    """
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                deep_merge(a[key], b[key], path + [str(key)])
            elif isinstance(a[key], (int, float, str, bool)) and isinstance(b[key], (int, float, str, bool)):
                a[key] = b[key]
            else:
                raise Exception("Conflict at %s" % ".".join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

def keys_exists(element: Dict[Any, Any], *keys: Union[str, int]) -> bool:
    """
    Check if *keys (nested) exists in `element` (dict).
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
