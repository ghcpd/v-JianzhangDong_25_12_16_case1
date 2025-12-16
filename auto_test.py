import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
VENV = ROOT / ".venv"
LOGS = ROOT / "logs"
LOGS.mkdir(exist_ok=True)
LOGFILE = LOGS / "test_run.log"

if os.name == "nt":
    venv_py = VENV / "Scripts" / "python.exe"
else:
    venv_py = VENV / "bin" / "python"

if not venv_py.exists():
    print("ERROR: .venv not found or not created. Create it and install requirements first:")
    print("  python -m venv .venv && .venv\\Scripts\\activate && pip install -r requirements.txt")
    sys.exit(2)

results = {
    "start_time": datetime.utcnow().isoformat() + "Z",
    "app": {},
    "tests": []
}

# 1) Start the application (it prints and exits)
env = os.environ.copy()
env["APP_MODE"] = "production"
proc = subprocess.run([str(venv_py), str(ROOT / "app.py")], capture_output=True, text=True, env=env)
results["app"] = {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}

# 2) Execute each test script by importing and running functions named test_*
tests_dir = ROOT / "tests"
for p in sorted(tests_dir.glob("test_*.py")) + sorted(tests_dir.glob("case_*.py")):
    # Build a small runner that loads the module and executes test_ functions
    runner = ROOT / "test_runner.py"
    proc = subprocess.run([str(venv_py), str(runner), str(p)], capture_output=True, text=True)
    test_result = {
        "file": str(p.relative_to(ROOT)),
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr
    }
    results["tests"].append(test_result)

# Write human-readable log
with LOGFILE.open("w", encoding="utf-8") as fh:
    fh.write(f"Test run: {results['start_time']}\n")
    fh.write("\n=== Application start ===\n")
    fh.write(f"returncode: {results['app']['returncode']}\n")
    fh.write("stdout:\n")
    fh.write(results['app']['stdout'] or "<no stdout>\n")
    fh.write("stderr:\n")
    fh.write(results['app']['stderr'] or "<no stderr>\n")
    fh.write("\n=== Tests ===\n")
    for t in results['tests']:
        fh.write(f"- {t['file']}: returncode={t['returncode']}\n")
        if t['stdout']:
            fh.write("  stdout:\n")
            fh.write(t['stdout'] + "\n")
        if t['stderr']:
            fh.write("  stderr:\n")
            fh.write(t['stderr'] + "\n")

# Exit non-zero if app failed or any tests failed
any_test_failures = any(t['returncode'] != 0 for t in results['tests'])
if results['app']['returncode'] != 0 or any_test_failures:
    print(f"Some checks failed. See {LOGFILE} for details.")
    sys.exit(1)

print(f"All checks passed. Log written to {LOGFILE}")
