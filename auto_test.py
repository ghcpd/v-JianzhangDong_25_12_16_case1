import subprocess
import sys
import os
from pathlib import Path

# Set the required environment variable for the app to run in production mode
os.environ['APP_MODE'] = 'production'

# Get the project root directory
project_root = Path(__file__).parent
logs_dir = project_root / 'logs'

# Create logs directory if it doesn't exist
logs_dir.mkdir(exist_ok=True)

# Path to the test log file
log_file = logs_dir / 'test_run.log'

# Get the Python executable from the .venv
venv_python = project_root / '.venv' / 'Scripts' / 'python.exe'

# Start the application in the background
print("Starting the application...")
app_process = subprocess.Popen(
    [str(venv_python), str(project_root / 'app.py')],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    cwd=str(project_root)
)

# Give the app a moment to start
import time
time.sleep(1)

# Run all test files
test_files = sorted((project_root / 'tests').glob('case_*.py'))

test_results = []

print(f"Running {len(test_files)} test files...")

for test_file in test_files:
    print(f"  - Running {test_file.name}...")
    result = subprocess.run(
        [str(venv_python), str(test_file)],
        capture_output=True,
        text=True,
        cwd=str(project_root)
    )
    
    test_results.append({
        'file': test_file.name,
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr
    })

# Terminate the app process
app_process.terminate()
app_process.wait(timeout=5)

# Write test results to log file
with open(log_file, 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("TEST RUN RESULTS\n")
    f.write("=" * 80 + "\n\n")
    
    for result in test_results:
        f.write(f"Test File: {result['file']}\n")
        f.write("-" * 80 + "\n")
        f.write(f"Return Code: {result['returncode']}\n\n")
        
        if result['stdout']:
            f.write("STDOUT:\n")
            f.write(result['stdout'])
            f.write("\n")
        
        if result['stderr']:
            f.write("STDERR:\n")
            f.write(result['stderr'])
            f.write("\n")
        
        f.write("\n")
    
    f.write("=" * 80 + "\n")
    f.write("TEST RUN COMPLETED\n")
    f.write("=" * 80 + "\n")

print(f"Test results written to {log_file}")
print("Done!")
