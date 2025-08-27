import ast
import os
from typing import List, Dict, Iterable


def _iter_python_files(
    roots: Iterable[str], patterns: Iterable[str] = ("*.py",), excludes: Iterable[str] = ()
) -> Iterable[str]:
    import fnmatch
    excludes = set(os.path.abspath(p) for p in excludes)
    for root in roots:
        root = os.path.abspath(root)
        for dirpath, dirnames, filenames in os.walk(root):
            # skip excluded dirs/files
            if any(os.path.abspath(dirpath).startswith(ex) for ex in excludes):
                continue
            for fname in filenames:
                if any(fnmatch.fnmatch(fname, pat) for pat in patterns):
                    fpath = os.path.join(dirpath, fname)
                    if any(os.path.abspath(fpath).startswith(ex) for ex in excludes):
                        continue
                    yield fpath


def parse_functions_from_paths(
    include_paths: List[str],
    file_globs: List[str],
    exclude_paths: List[str]
) -> List[Dict]:
    """
    Returns a list of function metadata dicts:
    { module_path, module_import, name, args, doc }
    """
    results: List[Dict] = []
    for file_path in _iter_python_files(include_paths, file_globs, exclude_paths):
        # ignore __init__.py and generated tests
        if os.path.basename(file_path).startswith("test_"):
            continue
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                src = f.read()
            tree = ast.parse(src)
        except Exception:
            continue

        rel_module = os.path.splitext(os.path.relpath(file_path).replace(os.sep, "."))[0]
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                doc = ast.get_docstring(node) or "No description provided."
                arg_names = [a.arg for a in node.args.args]
                results.append(
                    {
                        "module_path": file_path,
                        "module_import": rel_module,
                        "name": node.name,
                        "args": arg_names,
                        "doc": doc,
                    }
                )
    return results
