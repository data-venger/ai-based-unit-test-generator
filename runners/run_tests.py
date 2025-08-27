import argparse
import os

from core.coverage_runner import run_pytest_with_coverage
from reporting.coverage_reporter import summarize_coverage
from reporting.report_formater import summarize_pytest, write_human_readable


def main():
    parser = argparse.ArgumentParser(description="Run pytest with coverage and create a summary.")
    parser.add_argument("--report-dir", default="reporting")
    args = parser.parse_args()

    code, output = run_pytest_with_coverage(report_dir=args.report_dir)
    print(output)

    pytest_stats = summarize_pytest(os.path.join(args.report_dir, "pytest_report.json"))
    coverage_stats = summarize_coverage(os.path.join(args.report_dir, "coverage.xml"))
    summary_path = write_human_readable(args.report_dir, pytest_stats, coverage_stats)
    print(f"\nSummary written to: {summary_path}")
    if code != 0:
        # propagate failure
        raise SystemExit(code)


if __name__ == "__main__":
    main()
