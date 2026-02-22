# Main methond to start the process
import subprocess, sys

def main():
    print("==> Generating tests via Ollama...")
    gen = subprocess.run([sys.executable, "-m", "runners.generate_tests"], text=True)
    if gen.returncode != 0:
        raise SystemExit(gen.returncode)

    print("\n==> Running pytest + coverage...")
    run = subprocess.run([sys.executable, "-m", "runners.run_tests"], text=True)
    raise SystemExit(run.returncode)

if __name__ == "__main__":
    main()
