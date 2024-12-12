import os
import pytest
from utility.file_dir import FileFinder

@pytest.fixture
def temp_directory(tmp_path):
    # Create test files and directories
    test_files = [
        'test1.txt',
        'test2.txt',
        'test3.pdf',
        'subdir/test4.txt',
        'subdir/test5.pdf'
    ]
    
    for file_path in test_files:
        full_path = tmp_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.touch()
    
    return tmp_path

def test_find_all_files(temp_directory):
    finder = FileFinder(temp_directory)
    files = finder.find_all_files()
    
    # Should find all 5 files
    assert len(files) == 5
    
    # Convert paths to set of basenames for easier comparison
    file_names = {os.path.basename(f) for f in files}
    expected_names = {'test1.txt', 'test2.txt', 'test3.pdf', 'test4.txt', 'test5.pdf'}
    assert file_names == expected_names

def test_find_by_extension(temp_directory):
    finder = FileFinder(temp_directory)
    
    # Test .txt files
    txt_files = finder.find_by_extension('.txt')
    assert len(txt_files) == 3
    txt_names = {os.path.basename(f) for f in txt_files}
    assert txt_names == {'test1.txt', 'test2.txt', 'test4.txt'}
    
    # Test .pdf files
    pdf_files = finder.find_by_extension('.pdf')
    assert len(pdf_files) == 2
    pdf_names = {os.path.basename(f) for f in pdf_files}
    assert pdf_names == {'test3.pdf', 'test5.pdf'}

def test_get_file_count(temp_directory):
    finder = FileFinder(temp_directory)
    assert finder.get_file_count() == 5

def test_empty_directory(tmp_path):
    finder = FileFinder(tmp_path)
    assert finder.get_file_count() == 0
    assert len(finder.find_all_files()) == 0
    assert len(finder.find_by_extension('.txt')) == 0
