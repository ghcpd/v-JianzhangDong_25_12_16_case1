import subprocess
import sys

def test_app_starts():
    result = subprocess.run(
        [sys.executable, "app.py"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
