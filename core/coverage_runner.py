import subprocess
import os
from typing import Tuple


def run_pytest_with_coverage(report_dir: str = "reporting") -> Tuple[int, str]:
    """
    Executes pytest with coverage and json report.
    Returns (exit_code, combined_stdout_stderr).
    """
    os.makedirs(report_dir, exist_ok=True)

    cmd = [
        "python", "-m", "pytest",
        "--maxfail=1",
        "-q",
        "--disable-warnings",
        "--cov=my_codes",
        f"--cov-report=xml:{os.path.join(report_dir, 'coverage.xml')}",
        "--json-report",
        f"--json-report-file={os.path.join(report_dir, 'pytest_report.json')}",
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out
