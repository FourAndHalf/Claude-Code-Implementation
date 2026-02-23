from app.helpers.tool import tool
from pathlib import Path

SAFE_ROOT = Path.cwd()


@tool(tags=["filesystem"])
def read_file(file_path: str) -> str:
    """Read file from a given file path passed as argument"""

    p = (SAFE_ROOT / file_path).resolve()

    if not str(p).startswith(str(SAFE_ROOT)):
        raise ValueError("Access outside workspace not allowed")

    return p.read_text()
