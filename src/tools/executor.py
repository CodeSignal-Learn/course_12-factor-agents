import subprocess
import sys


def execute_python_code(code: str) -> dict:
    """
    Execute Python code and return stdout and stderr.
    
    Args:
        code (str): Python code to execute
        
    Returns:
        dict: Dictionary with keys 'stdout', 'stderr', and 'returncode'
        
    Raises:
        subprocess.TimeoutExpired: If execution exceeds timeout
    """
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }

