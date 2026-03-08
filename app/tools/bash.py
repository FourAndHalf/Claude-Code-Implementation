import subprocess
from app.helpers.tool import tool
from pathlib import Path

SAFE_ROOT = Path.cwd()

@tool(tags=["system"])
def bash(command: str) -> str:
    """Execute a bash command in the terminal and return its output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=SAFE_ROOT,
            capture_output=True,
            text=True,
            check=False
        )
        
        output = f"Exit Code: {result.returncode}\n"
        if result.stdout:
            output += f"Stdout:\n{result.stdout}\n"
        if result.stderr:
            output += f"Stderr:\n{result.stderr}\n"
            
        return output
    except Exception as e:
        return f"Error executing command: {str(e)}"
