import pytest
from utility.formater import toman, mask

def test_toman():
    # Test integer input
    assert toman(1000) == "1,000"
    assert toman(1000000) == "1,000,000"
    
    # Test float input
    assert toman(1000.50) == "1,000"  # Should round up
    assert toman(1000.49) == "1,000"  # Should round down
    
    # Test string input
    assert toman("1000") == "1,000"
    assert toman("1000.50") == "1,000"

def test_mask():
    # Test default masking (last 3 chars)
    assert mask("1234567890") == "1234567***"
    assert mask("ABC123") == "ABC***"
    
    # Test custom masking
    assert mask("1234567890", -4) == "123456****"
    assert mask("ABC123", -2) == "ABC1**"
    
    # Test edge cases
    assert mask("123") == "***"  # All masked with default
    assert mask("12", -3) == "**"  # Input shorter than mask length
