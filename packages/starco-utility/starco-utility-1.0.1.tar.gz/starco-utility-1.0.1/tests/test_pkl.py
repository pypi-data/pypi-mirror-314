import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utility.pkl import Pkl
import time

def test_pkl_basic():
    # Initialize with test file
    pkl_handler = Pkl(path='test_storage.pkl')
    
    # Test writing and reading
    print("1. Basic Write/Read Test")
    pkl_handler.pkl('test_key', 'test_value')
    result = pkl_handler.pkl('test_key')
    print(f"Written: test_value, Read: {result}")
    assert result == 'test_value'

def test_pkl_encrypted():
    # Initialize with encryption
    pkl_handler = Pkl(path='test_storage_encrypted.pkl', encrypt=True)
    
    # Test encrypted writing and reading
    print("\n2. Encrypted Write/Read Test")
    pkl_handler.pkl('secret_key', 'secret_value')
    result = pkl_handler.pkl('secret_key')
    print(f"Written: secret_value, Read: {result}")
    assert result == 'secret_value'

def test_pkl_expiration():
    # Initialize for expiration test
    pkl_handler = Pkl(path='test_storage_expir.pkl')
    
    # Test expiration
    print("\n3. Expiration Test")
    pkl_handler.pkl('expiring_key', 'expiring_value')
    
    # Read with 2 second expiration
    result1 = pkl_handler.pkl('expiring_key', expir_sec=2)
    print(f"Before expiration: {result1}")
    
    # Wait 3 seconds
    time.sleep(3)
    
    # Should return empty string after expiration
    result2 = pkl_handler.pkl('expiring_key', expir_sec=2)
    print(f"After expiration: {result2}")
    assert result2 == ''

def cleanup():
    # Clean up test files
    test_files = ['test_storage.pkl', 'test_storage_encrypted.pkl', 'test_storage_expir.pkl']
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)

if __name__ == "__main__":
    try:
        test_pkl_basic()
        test_pkl_encrypted()
        test_pkl_expiration()
        print("\nAll tests passed successfully!")
    finally:
        cleanup()
