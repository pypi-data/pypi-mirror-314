import pytest
from utility.structures import chunks, sort_dict_by_key, sort_dict_by_val


def test_chunks_with_list_integer_size():
    assert chunks(list(range(5)), 2) == [[0, 1], [2, 3], [4]]
    assert chunks(list(range(6)), 3) == [[0, 1, 2], [3, 4, 5]]

def test_chunks_with_list_tuple_size():
    assert chunks(list(range(5)), (2, 2)) == [[0, 1], [2, 3], [4]]
    assert chunks(list(range(6)), (2, 2, 2)) == [[0, 1], [2, 3], [4, 5]]

def test_chunks_with_reverse():
    assert chunks(list(range(4)), 2, reverse=True) == [[1, 0], [3, 2]]
    assert chunks(list(range(5)), (2, 2), reverse=True) == [[1, 0], [3, 2], [4]]

def test_chunks_with_dict():
    test_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    expected = [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}]
    assert chunks(test_dict, 2) == expected

def test_chunks_with_dict_and_reverse():
    test_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    expected = [{'b': 2, 'a': 1}, {'d': 4, 'c': 3}]
    assert chunks(test_dict, 2, reverse=True) == expected

def test_chunks_with_append_last():
    assert chunks(list(range(5)), (2, 2), append_last=True) == [[0, 1], [2, 3], [4]]
    assert chunks(list(range(5)), (2, 2), append_last=False) == [[0, 1], [2, 3]]

def test_empty_input():
    assert chunks([], 2) == []
    assert chunks({}, 2) == []

def test_sort_dict_by_key():
    test_dict = {'c': 1, 'a': 2, 'b': 3}
    
    # Test ascending
    assert list(sort_dict_by_key(test_dict).keys()) == ['a', 'b', 'c']
    
    # Test descending
    assert list(sort_dict_by_key(test_dict, reverse=True).keys()) == ['c', 'b', 'a']

def test_sort_dict_by_val():
    test_dict = {'a': 3, 'b': 1, 'c': 2}
    
    # Test ascending
    assert list(sort_dict_by_val(test_dict).values()) == [1, 2, 3]
    
    # Test descending 
    assert list(sort_dict_by_val(test_dict, reverse=True).values()) == [3, 2, 1]
