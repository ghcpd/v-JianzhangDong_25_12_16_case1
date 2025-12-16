import os
import subprocess
import sys
from pathlib import Path

# Determine the python executable inside the .venv
def get_venv_python():
    # Support Windows and POSIX
    venv_dir = Path('.venv')
    if not venv_dir.exists():
        raise RuntimeError('.venv directory not found. Create the virtual environment first.')
    if os.name == 'nt':
        # On Windows the executable is usually python.exe
        python_path = venv_dir / 'Scripts' / 'python.exe'
        if not python_path.exists():
            # fall back to 'python' in case of unusual naming
            python_path = venv_dir / 'Scripts' / 'python'
    else:
        python_path = venv_dir / 'bin' / 'python'
    if not python_path.exists():
        raise RuntimeError(f'Python executable not found at {python_path}')
    return str(python_path)

LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)
log_file = LOG_DIR / 'test_run.log'

def write_log(message: str):
    with log_file.open('a', encoding='utf-8') as f:
        f.write(message + '\n')

python_exe = get_venv_python()

# 1) Start the application
write_log('=== Running app.py using .venv Python ===')
result = subprocess.run([python_exe, 'app.py'], capture_output=True, text=True, env={**os.environ, 'APP_MODE': 'production'})
write_log('Return code: ' + str(result.returncode))
write_log('STDOUT:\n' + result.stdout)
write_log('STDERR:\n' + result.stderr)

# 2) Run tests using pytest (install if needed)
write_log('\n=== Running tests with pytest ===')
# Ensure pytest is installed in the venv; install it if missing
try:
    result = subprocess.run([python_exe, '-m', 'pytest', '--version'], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError('pytest not available')
except Exception:
    write_log('pytest not found in .venv; installing pytest...')
    subprocess.run([python_exe, '-m', 'pip', 'install', 'pytest'], check=True)

# Explicitly run pytest on all .py files in tests/ so files that don't match the default
# pytest naming pattern are still executed
import glob

pytest_files = glob.glob(os.path.join('tests', '*.py'))
pytest_cmd = [python_exe, '-m', 'pytest', '-q'] + pytest_files
result = subprocess.run(pytest_cmd, capture_output=True, text=True, env={**os.environ, 'APP_MODE': 'production'})
write_log('Return code: ' + str(result.returncode))
write_log('STDOUT:\n' + result.stdout)
write_log('STDERR:\n' + result.stderr)

print(f'Wrote logs to {log_file}')
