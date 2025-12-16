import subprocess
import sys

def test_output_contains_port():
    result = subprocess.run(
        [sys.executable, "app.py"],
        capture_output=True,
        text=True
    )
    assert "Port:" in result.stdout
