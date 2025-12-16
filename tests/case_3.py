import subprocess
import sys

def test_correct_port():
    result = subprocess.run(
        [sys.executable, "app.py"],
        capture_output=True,
        text=True
    )
    assert "9123" in result.stdout
