import os
from lxml import etree


def summarize_coverage(xml_path: str) -> dict:
    """
    Reads coverage.xml and returns summary stats.
    """
    if not os.path.exists(xml_path):
        return {"error": f"{xml_path} not found"}
    tree = etree.parse(xml_path)
    root = tree.getroot()
    # Cobertura-like format
    lines_valid = int(root.get("lines-valid", "0"))
    lines_covered = int(root.get("lines-covered", "0"))
    branch_rate = float(root.get("branch-rate", "0.0"))
    line_rate = float(root.get("line-rate", "0.0"))
    return {
        "lines_valid": lines_valid,
        "lines_covered": lines_covered,
        "line_rate": round(line_rate * 100, 2),
        "branch_rate": round(branch_rate * 100, 2),
    }
