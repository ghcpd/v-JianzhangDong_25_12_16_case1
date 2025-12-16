import os
import shutil
import subprocess
import sys
from pathlib import Path
import venv
import time

ROOT = Path(__file__).parent
VENV_DIR = ROOT / '.venv'
LOG_DIR = ROOT / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'test_run.log'

PYTHON = str(VENV_DIR / 'Scripts' / 'python.exe') if os.name == 'nt' else str(VENV_DIR / 'bin' / 'python')


def run(cmd, env=None, check=True, capture_output=False, text=True):
    print('Running:', ' '.join(cmd))
    return subprocess.run(cmd, env=env, check=check, capture_output=capture_output, text=text)


def recreate_venv():
    if VENV_DIR.exists():
        print('Removing existing .venv')
        shutil.rmtree(VENV_DIR)

    print('Creating new virtual environment at', VENV_DIR)
    venv.create(VENV_DIR, with_pip=True)

    print('Installing required packages')
    run([PYTHON, '-m', 'pip', 'install', '--upgrade', 'pip'])
    run([PYTHON, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    run([PYTHON, '-m', 'pip', 'install', 'pytest'])


def start_service(env):
    # Start app.py with APP_MODE=production in background, capture output
    proc = subprocess.Popen([PYTHON, 'app.py'], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print('Started service, PID=', proc.pid)
    # allow some time to start
    time.sleep(0.5)
    return proc


def run_tests(env):
    print('Running pytest...')
    # Explicitly collect files matching tests/case_*.py to handle non-standard test filenames
    test_dir = ROOT / 'tests'
    files = sorted([str(p) for p in test_dir.glob('case_*.py')])
    print('Detected test files:', files)
    if files:
        cmd = [PYTHON, '-m', 'pytest', '-q'] + files
    else:
        cmd = [PYTHON, '-m', 'pytest', '-q', 'tests']
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    return result


def main():
    recreate_venv()

    # Prepare environment for running service and tests
    env = os.environ.copy()
    env['APP_MODE'] = 'production'

    # Start the service
    svc = start_service(env)

    try:
        result = run_tests(env)
    finally:
        # Attempt to terminate service
        try:
            svc.terminate()
            svc.wait(timeout=2)
        except Exception:
            try:
                svc.kill()
            except Exception:
                pass

    # Write logs
    with LOG_FILE.open('w', encoding='utf-8') as f:
        f.write('--- SERVICE STDOUT (partial) ---\n')
        try:
            out = svc.stdout.read() if svc.stdout else ''
        except Exception:
            out = ''
        f.write((out or '') + '\n')
        f.write('--- PYTEST STDOUT ---\n')
        f.write(result.stdout or '')
        f.write('\n--- PYTEST STDERR ---\n')
        f.write(result.stderr or '')

    print('Test run complete. Log written to', LOG_FILE)

    if result.returncode != 0:
        print('Tests failed with return code', result.returncode)
        sys.exit(result.returncode)


if __name__ == '__main__':
    main()
