import pytest
import os
import tempfile
from pathlib import Path
from utility.file_dir import ZipUtility

class TestZipUtility:
    @pytest.fixture
    def setup_test_env(self):
        # Create temporary directory for tests
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files and directories
            test_dir = Path(temp_dir)
            
            # Create test files
            (test_dir / "file1.txt").write_text("Test content 1")
            (test_dir / "file2.txt").write_text("Test content 2")
            
            # Create nested directory with files
            nested_dir = test_dir / "nested"
            nested_dir.mkdir()
            (nested_dir / "nested_file.txt").write_text("Nested content")
            
            yield test_dir
    
    @pytest.fixture
    def zip_utility(self):
        return ZipUtility()
    
    def test_zip_single_file(self, setup_test_env, zip_utility):
        test_dir = setup_test_env
        source_file = test_dir / "file1.txt"
        zip_name = test_dir / "single_file.zip"
        
        # Test zip creation
        result = zip_utility.zip_files(str(source_file), str(zip_name))
        assert result == True
        assert zip_name.exists()
        
        # Verify zip contents
        info = zip_utility.get_zip_info(str(zip_name))
        assert info['file_count'] == 1
        assert info['files'][0]['filename'] == "file1.txt"
    
    def test_zip_multiple_files(self, setup_test_env, zip_utility):
        test_dir = setup_test_env
        source_files = [
            str(test_dir / "file1.txt"),
            str(test_dir / "file2.txt")
        ]
        zip_name = test_dir / "multiple_files.zip"
        
        result = zip_utility.zip_files(source_files, str(zip_name))
        assert result == True
        
        info = zip_utility.get_zip_info(str(zip_name))
        assert info['file_count'] == 2
    
    def test_zip_directory(self, setup_test_env, zip_utility):
        test_dir = setup_test_env
        zip_name = test_dir / "directory.zip"
        
        result = zip_utility.zip_files(str(test_dir / "nested"), str(zip_name))
        assert result == True
        
        info = zip_utility.get_zip_info(str(zip_name))
        assert info['file_count'] == 1
        assert any("nested_file.txt" in file['filename'] for file in info['files'])
    
    def test_unzip_files(self, setup_test_env, zip_utility):
        test_dir = setup_test_env
        source_file = test_dir / "file1.txt"
        zip_name = test_dir / "test_unzip.zip"
        extract_dir = test_dir / "extracted"
        
        # Create zip first
        zip_utility.zip_files(str(source_file), str(zip_name))
        
        # Test extraction
        result = zip_utility.unzip_files(str(zip_name), str(extract_dir))
        assert result == True
        assert (extract_dir / "file1.txt").exists()
        assert (extract_dir / "file1.txt").read_text() == "Test content 1"
    
    def test_get_zip_info(self, setup_test_env, zip_utility):
        test_dir = setup_test_env
        source_file = test_dir / "file1.txt"
        zip_name = test_dir / "info_test.zip"
        
        zip_utility.zip_files(str(source_file), str(zip_name))
        
        info = zip_utility.get_zip_info(str(zip_name))
        assert info is not None
        assert 'file_count' in info
        assert 'total_size' in info
        assert 'compressed_size' in info
        assert 'files' in info
        assert len(info['files']) == 1
    
    def test_invalid_zip_operations(self, setup_test_env, zip_utility):
        test_dir = setup_test_env
        
        # Test non-existent source
        result = zip_utility.zip_files("nonexistent.txt", "test.zip")
        assert result == False
        
        # Test invalid zip file for extraction
        result = zip_utility.unzip_files("nonexistent.zip")
        assert result == False
        
        # Test invalid zip file for info
        info = zip_utility.get_zip_info("nonexistent.zip")
        assert info is None
