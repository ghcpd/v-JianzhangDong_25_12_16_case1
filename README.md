## Requirements

- Python 3.10+
- pip

---

## Quick Start

These instructions are for Windows. Adjust activation commands for other OSes.

### 1. Create a clean virtual environment

We use a project-local virtual environment named `.venv`.

```powershell
# Remove any existing virtualenv and create a fresh one
if (Test-Path -Path .venv) { Remove-Item -Recurse -Force .venv }
python -m venv .venv
.\.venv\Scripts\Activate
```

Note: Do not reuse other virtual environments — this project expects a fresh `.venv` folder.

### 2. Install dependencies

With `.venv` activated run:

```
pip install -r requirements.txt
pip install pytest
```

(We install pytest here so tests can be executed.)

### 3. Configure environment variables

```
copy .env.example .env
```

Edit `.env` and set the following values (important):
```
# Use "production" mode so the service will start
APP_MODE=production
```

This project reads the PORT from `settings.yaml` (the default value is 9123). The code requires APP_MODE to be set to "production".

### 4. Run the application

Start the service with:

```
python app.py
```

If environment and configuration are correct the program will print:

```
Service started successfully
Port: 9123
```

### 5. Run the test suite (and collect logs)

A convenience script `auto_test.py` is provided to:
- create/prepare `.venv` (if necessary),
- install dependencies inside `.venv`,
- start the service with APP_MODE=production,
- run all tests under `tests/` using the `.venv` Python, and
- write test output to `logs/test_run.log`.

Run it with:

```
python auto_test.py
```

Logs will be available at `logs/test_run.log`.

---

If you encounter issues, make sure `settings.yaml` exists and contains a valid integer port under `service.port`, and that your `.env` file contains `APP_MODE=production`.