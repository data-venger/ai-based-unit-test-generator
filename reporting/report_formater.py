import json
import os
from typing import Dict


def summarize_pytest(json_path: str) -> Dict:
    if not os.path.exists(json_path):
        return {"error": f"{json_path} not found"}
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    summary = data.get("summary", {})
    return {
        "collected": summary.get("collected", 0),
        "passed": summary.get("passed", 0),
        "failed": summary.get("failed", 0),
        "skipped": summary.get("skipped", 0),
        "xfailed": summary.get("xfailed", 0),
        "xpassed": summary.get("xpassed", 0),
        "errors": summary.get("errors", 0),
        "duration_seconds": data.get("duration", 0.0),
    }


def write_human_readable(report_dir: str, pytest_stats: Dict, coverage_stats: Dict) -> str:
    os.makedirs(report_dir, exist_ok=True)
    out_path = os.path.join(report_dir, "summary.txt")
    lines = []
    lines.append("=== Pytest Summary ===")
    for k in ["collected", "passed", "failed", "errors", "skipped", "xfailed", "xpassed", "duration_seconds"]:
        lines.append(f"{k:>16}: {pytest_stats.get(k)}")
    lines.append("")
    lines.append("=== Coverage Summary ===")
    if "error" in coverage_stats:
        lines.append(coverage_stats["error"])
    else:
        lines.append(f"{'Lines Covered':>16}: {coverage_stats['lines_covered']} / {coverage_stats['lines_valid']}")
        lines.append(f"{'Line Rate':>16}: {coverage_stats['line_rate']}%")
        lines.append(f"{'Branch Rate':>16}: {coverage_stats['branch_rate']}%")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return out_path
