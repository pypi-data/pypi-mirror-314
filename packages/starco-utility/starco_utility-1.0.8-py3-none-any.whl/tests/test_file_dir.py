import os
import shutil
import pytest
from utility.file_dir import directory_creator, root_path

@pytest.fixture
def temp_test_dir():
    # Create temporary test directory
    test_dir = "test_temp_dir"
    os.environ['root_path'] = test_dir
    yield test_dir
    # Cleanup after tests
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    if 'root_path' in os.environ:
        del os.environ['root_path']

def test_root_path():
    # Test default behavior (getcwd)
    assert root_path() == os.getcwd()
    
    # Test with environment variable
    test_path = "/test/path"
    os.environ['root_path'] = test_path
    assert root_path() == test_path
    del os.environ['root_path']

def test_directory_creator_with_string(temp_test_dir):
    # Test with single directory string
    test_dir = "test_dir1"
    base_path = directory_creator(test_dir, temp_test_dir)
    assert os.path.exists(f"{temp_test_dir}/{test_dir}")
    assert base_path == temp_test_dir

def test_directory_creator_with_list(temp_test_dir):
    # Test with list of directories
    test_dirs = ["test_dir2", "test_dir3/nested"]
    base_path = directory_creator(test_dirs, temp_test_dir)
    for dir_path in test_dirs:
        assert os.path.exists(f"{temp_test_dir}/{dir_path}")
    assert base_path == temp_test_dir
