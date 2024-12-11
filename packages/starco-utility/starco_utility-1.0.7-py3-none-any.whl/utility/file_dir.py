import os

from pathlib import Path
import os
from pathlib import Path
import zipfile

def root_path():
    """
    Returns the root path of the project.

    Returns:
        str: The root path of the project.
    """
    return os.environ.get('root_path') or os.getcwd()

import os,sys

def get_script_path():
    return os.path.abspath(sys.modules['__main__'].__file__)



def directory_creator(path:list|str,root_path:str=root_path()):
    """
    Creates directories from a list starting from project base path
    
    Args:
        path:list|str (list): List of directory names to create
        
    Returns:
        bool: base_path
    """
    if isinstance(path, str):
        path = [path]
    for directory in path:
        full_path = f"{root_path}/{directory}"
        full_path=Path(full_path)
        try:
            full_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Error creating directory {directory}: {str(e)}")
            input()
    return root_path



class ZipUtility:
    def __init__(self, base_path: str = None):
        self.base_path = base_path or root_path()

    def zip_files(self, source_path: str|list, zip_name: str, compression_level: int = 8) -> bool:
        """
        Zip files or directories into a ZIP archive
        
        Args:
            source_path: Path(s) to files/directories to zip
            zip_name: Name of the output ZIP file
            compression_level: ZIP compression level (0-9, default 8)
            
        Returns:
            bool: Success status
        """
        try:
            if isinstance(source_path, str):
                source_path = [source_path]
            # Check if all source paths exist
            for path in source_path:
                full_path = os.path.join(self.base_path, path)
                if not os.path.exists(full_path):
                    print(f"Error: Path does not exist: {full_path}")
                    return False
            # Ensure zip_name has .zip extension
            if not zip_name.endswith('.zip'):
                zip_name += '.zip'
                
            zip_path = os.path.join(self.base_path, zip_name)
            
            with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, 
                               compresslevel=compression_level) as zipf:
                
                for path in source_path:
                    full_path = os.path.join(self.base_path, path)
                    
                    if os.path.isfile(full_path):
                        # Add single file
                        zipf.write(full_path, os.path.basename(full_path))
                    elif os.path.isdir(full_path):
                        # Add directory contents
                        for root, _, files in os.walk(full_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, self.base_path)
                                zipf.write(file_path, arcname)
            return True
            
        except Exception as e:
            print(f"Error creating zip file: {str(e)}")
            return False

    def unzip_files(self, zip_path: str, extract_path: str = None, password: bytes = None) -> bool:
        """
        Extract ZIP archive contents
        
        Args:
            zip_path: Path to ZIP file
            extract_path: Extraction destination path (default: same as ZIP location)
            password: ZIP password if encrypted
            
        Returns:
            bool: Success status
        """
        try:
            full_zip_path = os.path.join(self.base_path, zip_path)
            
            if not extract_path:
                extract_path = os.path.dirname(full_zip_path)
            else:
                extract_path = os.path.join(self.base_path, extract_path)
                
            with zipfile.ZipFile(full_zip_path, 'r') as zipf:
                if password:
                    zipf.extractall(extract_path, pwd=password)
                else:
                    zipf.extractall(extract_path)
            return True
            
        except Exception as e:
            print(f"Error extracting zip file: {str(e)}")
            return False

    def get_zip_info(self, zip_path: str) -> dict:
        """
        Get information about ZIP archive contents
        
        Args:
            zip_path: Path to ZIP file
            
        Returns:
            dict: ZIP file information
        """
        try:
            full_zip_path = os.path.join(self.base_path, zip_path)
            info = {
                'file_count': 0,
                'total_size': 0,
                'compressed_size': 0,
                'files': []
            }
            
            with zipfile.ZipFile(full_zip_path, 'r') as zipf:
                for item in zipf.infolist():
                    info['file_count'] += 1
                    info['total_size'] += item.file_size
                    info['compressed_size'] += item.compress_size
                    info['files'].append({
                        'filename': item.filename,
                        'size': item.file_size,
                        'compressed_size': item.compress_size,
                        'date_time': item.date_time
                    })
            return info
            
        except Exception as e:
            print(f"Error getting zip info: {str(e)}")
            return None


import os
from pathlib import Path

class FileFinder:
    def __init__(self, directory):
        self.directory = directory
        
    def find_all_files(self):
        """Returns a list of all files in the directory and subdirectories"""
        files = []
        for root, dirs, filenames in os.walk(self.directory):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return files
    
    def find_by_extension(self, extension):
        """Returns a list of files with specific extension"""
        files = []
        for file in self.find_all_files():
            if file.endswith(extension):
                files.append(file)
        return files
    
    def get_file_count(self):
        """Returns total number of files"""
        return len(self.find_all_files())


