import pytest
from utility.structures import chunks, chunk_dict, sort_dict_by_key, sort_dict_by_val

def test_chunks():
    # Test regular chunks
    assert list(chunks([1,2,3,4,5], 2)) == [[1,2], [3,4], [5]]
    
    # Test with reverse=True
    result = chunks([1,2,3,4], 2, reverse=True)
    assert [list(x) for x in result] == [[2,1], [4,3]]
    
    # Test empty list
    assert list(chunks([], 3)) == []

def test_chunk_dict():
    test_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    
    # Test with limit 2
    result = chunk_dict(test_dict, 2)
    assert len(result) == 2
    assert result[0] == {'a': 1, 'b': 2}
    assert result[1] == {'c': 3, 'd': 4}
    
    # Test with limit larger than dict size
    assert chunk_dict(test_dict, 5) == [test_dict]

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
