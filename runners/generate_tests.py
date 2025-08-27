import argparse
import yaml
from core.function_parser import parse_functions_from_paths
from core.ollama_client import OllamaClient
from core.test_generator import generate_tests_for_functions


def main():
    parser = argparse.ArgumentParser(description="Generate pytest test files with Ollama.")
    parser.add_argument("--config", default="config/model_config.yaml")
    parser.add_argument("--tests-dir", default="tests")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    fns = parse_functions_from_paths(
        include_paths=cfg.get("include_paths", ["./"]),
        file_globs=cfg.get("file_globs", ["**/*.py"]),
        exclude_paths=cfg.get("exclude_paths", []),
    )
    print(fns)
    if not fns:
        print("No functions found to generate tests for.")
        return

    client = OllamaClient(
        endpoint=cfg["endpoint"],
        model=cfg["model"],
        temperature=cfg.get("temperature", 0.2),
    )
    created = generate_tests_for_functions(
        functions=fns,
        client=client,
        preamble=cfg.get("prompt_preamble", ""),
        tests_dir=args.tests_dir,
    )
    print(f"Generated {len(created)} test files:")
    for p in created:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
