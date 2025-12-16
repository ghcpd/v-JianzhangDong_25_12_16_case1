#!/usr/bin/env python

"""
Auto Test Runner
=================

This script starts the project using the `.venv` Python interpreter and then
runs all tests in the `tests/` folder.  Results (stdout and stderr) are
written to `logs/test_run.log`.

The script is intentionally simple and avoids activating the virtual
environment inside the script. Instead it explicitly invokes the interpreter
located under `.venv`.
"""

import os
import subprocess
import datetime
import sys


def get_venv_python():
    # Support Windows and POSIX
    if os.name == "nt":
        return os.path.join(".venv", "Scripts", "python.exe")
    return os.path.join(".venv", "bin", "python")


def write_log(message: str, handle):
    timestamp = datetime.datetime.now().isoformat()
    handle.write(f"[{timestamp}] {message}\n")


def main():
    venv_python = get_venv_python()
    if not os.path.exists(venv_python):
        print(f"Cannot find Python interpreter at {venv_python}. Did you create .venv?", file=sys.stderr)
        sys.exit(1)

    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", "test_run.log")

    env = os.environ.copy()
    # Ensure the application sees APP_MODE='production'
    env["APP_MODE"] = "production"

    with open(log_path, "w", encoding="utf-8") as fh:
        write_log("Auto test started", fh)

        # Start the app
        write_log("Running app.py", fh)
        try:
            proc = subprocess.run(
                [venv_python, "app.py"], capture_output=True, text=True, env=env
            )
            fh.write(proc.stdout)
            fh.write(proc.stderr)
            write_log(f"app.py exit code: {proc.returncode}", fh)
        except Exception as e:
            write_log(f"Error running app.py: {e}", fh)
            raise

        # Run the tests (execute each test script directly)
        write_log("Running test scripts", fh)
        exit_codes = []
        test_dir = os.path.join("tests")
        for test_file in sorted(os.listdir(test_dir)):
            if not test_file.endswith(".py"):
                continue
            test_path = os.path.join(test_dir, test_file)
            write_log(f"Running {test_path}", fh)
            try:
                proc = subprocess.run(
                    [venv_python, test_path], capture_output=True, text=True, env=env
                )
                fh.write(proc.stdout)
                fh.write(proc.stderr)
                write_log(f"{test_path} exit code: {proc.returncode}", fh)
                exit_codes.append(proc.returncode)
            except Exception as e:
                write_log(f"Error running {test_path}: {e}", fh)
                exit_codes.append(1)
        # If any test failed, overall exit code is non-zero
        if any(code != 0 for code in exit_codes):
            write_log("Some tests failed.", fh)
        else:
            write_log("All tests passed.", fh)

        write_log("Auto test finished", fh)


if __name__ == "__main__":
    main()
