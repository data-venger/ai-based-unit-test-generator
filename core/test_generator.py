import os
import textwrap
from typing import Dict, List

from .ollama_client import OllamaClient


START = ">>>PYTEST_START"
END = ">>>PYTEST_END"


def _build_prompt(preamble: str, fn: Dict) -> str:
    signature = f"{fn['name']}({', '.join(fn['args'])})"
    module_import = fn["module_import"]
    doc = textwrap.dedent(fn["doc"]).strip()
    return f"""{preamble}

Target:
- Module: {module_import}
- Function: {signature}
- Function docstring (description):
\"\"\"
{doc}
\"\"\"

Generate tests now.
Remember: output only the code between the markers.
{START}
"""


def _extract_code_between_markers(text: str) -> str:
    """
    Extracts code between PYTEST_START and PYTEST_END markers,
    removes Markdown code fences (```), and drops leftover markers.
    """
    if START in text and END in text:
        extracted = text.split(START, 1)[1].split(END, 1)[0].strip()
    else:
        extracted = text.strip()

    cleaned_lines = []
    for line in extracted.splitlines():
        stripped = line.strip()
        # 🚨 skip markers and code fences
        if stripped.startswith("```"):
            continue
        if stripped in (START, END):
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()






def generate_tests_for_functions(
    functions: List[Dict],
    client: OllamaClient,
    preamble: str,
    tests_dir: str = "tests",
) -> List[str]:
    os.makedirs(tests_dir, exist_ok=True)
    created_files = []
    for fn in functions:
        prompt = _build_prompt(preamble, fn)
        raw = client.generate(prompt)
        code = _extract_code_between_markers(raw)
        if not code.startswith("import") and "pytest" not in code:
            # minimal guard: wrap in a pytest file if LLM forgot
            code = f"import pytest\nfrom {fn['module_import']} import {fn['name']}\n\n" + code
        fname = f"test_{fn['name']}.py"
        out_path = os.path.join(tests_dir, fname)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(code.rstrip() + "\n")
        created_files.append(out_path)
    # ensure tests is a package for relative imports to resolve
    init_file = os.path.join(tests_dir, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w", encoding="utf-8") as f:
            f.write("# auto-generated\n")
    return created_files
