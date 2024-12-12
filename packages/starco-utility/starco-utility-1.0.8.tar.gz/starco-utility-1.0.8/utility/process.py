import os,signal,subprocess,psutil

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

class WindowsProcess:
    def __init__(self):
        pass
    @staticmethod
    def close_app(process_name="terminal64.exe"):
        """
        Closes the MetaTrader application by terminating its process.
        
        :param process_name: The name of the MetaTrader process (default is 'terminal.exe').
        """
        for process in psutil.process_iter(attrs=["pid", "name"]):
            if process.info["name"] == process_name:
                os.kill(process.info["pid"], signal.SIGTERM)
                print(f"Closed {process_name} with PID {process.info['pid']}")
                return
        print(f"Process {process_name} not found.")

    # Example usage

    @staticmethod
    def run_exe(file_path):
        """
        Runs an EXE file using the subprocess module.
        :param file_path: The path to the EXE file to execute.
        """
        try:
            # Start the EXE file as a new process
            process = subprocess.Popen(file_path, shell=True)
            print(f"File {file_path} is running with PID: {process.pid}")
            return True
        except FileNotFoundError:
            print("The specified file was not found.")
        except Exception as e:
            print(f"An error occurred while running the file: {e}")
        return False

    @staticmethod
    def run_exe_with_os(file_path):
        """
        Runs an EXE file using the os module.
        :param file_path: The path to the EXE file to execute.
        """
        try:
            # Start the EXE file
            os.startfile(file_path)
            print(f"File {file_path} is running.")
            return True
            
        except FileNotFoundError:
            print("The specified file was not found.")
        except Exception as e:
            print(f"An error occurred while running the file: {e}")
        return False