from app.helpers.tool import tool
from pathlib import Path

SAFE_ROOT = Path.cwd()

@tool(tags=["filesystem"])
def write_file(file_path: str, content: str) -> str:
    """Write content to a file at the given file path passed as argument"""

    p = (SAFE_ROOT / file_path).resolve()

    if not str(p).startswith(str(SAFE_ROOT)):
        raise ValueError("Access outside workspace not allowed")

    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    
    return "Success"
