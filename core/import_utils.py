import ast
from pathlib import Path

def get_imports(file_path: str) -> set[str]:
    """Return all imported modules from a Python file."""
    path = Path(file_path)
    tree = ast.parse(path.read_text())
    return {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    } | {
        alias.name.split('.')[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
