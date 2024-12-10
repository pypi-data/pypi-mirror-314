import psutil
import os

def is_script_running(script_path):
    """
    Check if a specific script is running by its exact path
    
    Args:
        script_path (str): Full path of the script to check
        
    Returns:
        dict: Information about running script (pid, path) or None if not running
    """
    script_abs_path = script_path
    result=[]
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            if proc.info['cmdline']:
                cmdline = ' '.join(proc.info['cmdline'])
                # Check for exact path match
                if script_abs_path in cmdline:
                    result+=[{
                        'pid': proc.info['pid'],
                        'path': cmdline
                    }]
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
            
    return result


import psutil
import os
import signal

def kill_script(script_path):
    """
    Kill a specific script running at given path
    
    Args:
        script_path (str): Full path of script to kill
        
    Returns:
        bool: True if killed successfully, False if not found/error
    """
    results = is_script_running(script_path)
    for result in results:
        try:
            os.kill(result['pid'], signal.SIGTERM)
            return True
        except ProcessLookupError:
            return False
    return False


import functools
import os
from .file_dir import get_script_path
def prevent_multiple_runs(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        script_path =get_script_path()
        runs =is_script_running(script_path)
        if len(runs)>1:
            print(f"Script {script_path} is already running. Skipping this run.")
            return None
        return func(*args, **kwargs)
    return wrapper
