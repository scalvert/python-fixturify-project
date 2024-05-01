import pytest
from python_fixturify_project.utils import deep_merge, keys_exists

def test_deep_merge_basic():
    a = {'x': 1, 'y': {'a': 1}}
    b = {'x': 2, 'y': {'b': 2}}
    expected = {'x': 2, 'y': {'a': 1, 'b': 2}}
    assert deep_merge(a, b) == expected

def test_deep_merge_same_leaf_value():
    a = {'x': 1, 'y': 1}
    b = {'x': 1, 'y': 1}
    expected = {'x': 1, 'y': 1}
    assert deep_merge(a, b) == expected

def test_deep_merge_conflict():
    a = {'x': 1}
    b = {'x': {'y': 2}}
    with pytest.raises(Exception) as e_info:
        deep_merge(a, b)
    assert str(e_info.value) == 'Conflict at x'

def test_deep_merge_empty_dicts():
    a = {}
    b = {}
    expected = {}
    assert deep_merge(a, b) == expected

def test_keys_exists_basic():
    d = {'x': 1, 'y': {'a': 1, 'b': 2}}
    assert keys_exists(d, 'x')
    assert keys_exists(d, 'y', 'a')
    assert not keys_exists(d, 'y', 'c')

def test_keys_exists_empty_dict():
    d = {}
    assert not keys_exists(d, 'x')

def test_keys_exists_non_dict_argument():
    with pytest.raises(AttributeError) as e_info:
        keys_exists([], 'x')
    assert str(e_info.value) == 'keys_exists() expects dict as first argument.'

def test_keys_exists_no_keys_provided():
    d = {'x': 1}
    with pytest.raises(AttributeError) as e_info:
        keys_exists(d)
    assert str(e_info.value) == 'keys_exists() expects at least two arguments, one given.'