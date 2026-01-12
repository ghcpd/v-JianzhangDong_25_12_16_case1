import os
import subprocess
import sys
from datetime import datetime

ROOT = os.path.dirname(__file__)
VENV_PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join(ROOT, ".venv", "bin", "python")
LOG_DIR = os.path.join(ROOT, "logs")
LOG_FILE = os.path.join(LOG_DIR, "test_run.log")

os.makedirs(LOG_DIR, exist_ok=True)

with open(LOG_FILE, "a", encoding="utf-8") as log:
    log.write(f"\n--- Test run at {datetime.utcnow().isoformat()}Z ---\n")

    if not os.path.exists(VENV_PY):
        msg = f"ERROR: virtualenv python not found at {VENV_PY}. Please create .venv first.\n"
        log.write(msg)
        print(msg, file=sys.stderr)
        sys.exit(2)

    # Ensure pytest is installed in venv
    log.write("Installing test dependencies (pytest) in .venv/ if missing...\n")
    subprocess.run([VENV_PY, "-m", "pip", "install", "pytest"], stdout=log, stderr=log, text=True)

    # Start the app once and capture its output
    log.write("\nRunning app (one-shot) to verify startup output...\n")
    env = os.environ.copy()
    env["APP_MODE"] = "production"
    log.write(f"Setting APP_MODE=production for test runs.\n")
    proc = subprocess.run([VENV_PY, os.path.join(ROOT, "app.py")], capture_output=True, text=True, env=env)
    log.write("--- app.py stdout ---\n")
    log.write(proc.stdout + "\n")
    log.write("--- app.py stderr ---\n")
    log.write(proc.stderr + "\n")
    log.write(f"app.py exit code: {proc.returncode}\n")

    # Run pytest using venv python with APP_MODE in environment
    log.write("\nRunning pytest tests/ (explicit case files) ...\n")
    tests_dir = os.path.join(ROOT, "tests")
    test_files = [os.path.join(tests_dir, f) for f in os.listdir(tests_dir) if f.startswith("case_") and f.endswith(".py")]
    if not test_files:
        log.write("No test files found matching pattern 'case_*.py' in tests/.\n")
        pytest_proc = subprocess.CompletedProcess(args=[], returncode=5, stdout="", stderr="No tests found")
    else:
        cmd = [VENV_PY, "-m", "pytest", "-q"] + test_files
        log.write(f"Running pytest on files: {test_files}\n")
        pytest_proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    log.write("--- pytest stdout ---\n")
    log.write(pytest_proc.stdout + "\n")
    log.write("--- pytest stderr ---\n")
    log.write(pytest_proc.stderr + "\n")
    log.write(f"pytest exit code: {pytest_proc.returncode}\n")

    # Summarize
    if proc.returncode == 0 and pytest_proc.returncode == 0:
        log.write("\nRESULT: SUCCESS - app started and tests passed.\n")
        print("Auto-test completed: SUCCESS")
        sys.exit(0)
    else:
        log.write("\nRESULT: FAILURE - check outputs above for details.\n")
        print("Auto-test completed: FAILURE (see logs/test_run.log)")
        sys.exit(1)
