import os
import subprocess

# Set environment variable
os.environ['APP_MODE'] = 'production'

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Run pytest using the .venv environment
result = subprocess.run(
    [r'.venv\Scripts\python', '-m', 'pytest', 'tests/case_1.py', 'tests/case_2.py', 'tests/case_3.py', '-v'],
    capture_output=True,
    text=True
)

# Write test results to log file
with open('logs/test_run.log', 'w') as f:
    f.write('STDOUT:\n')
    f.write(result.stdout)
    f.write('\nSTDERR:\n')
    f.write(result.stderr)
    f.write(f'\nReturn code: {result.returncode}\n')