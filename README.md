## Requirements

- Python 3.10+
- pip

---

## Quick Start

### 1. Create virtual environment

```bash
python -m venv .venv
```

Activate it in PowerShell (recommended):

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on cmd:

```bat
.\.venv\Scripts\activate.bat
```

### 2. Install dependencies

If you activated the virtual environment above you can simply run:

```bash
pip install -r requirements.txt
```

Otherwise, use the environment's python executable directly:

```bash
.\.venv\Scripts\python -m pip install -r requirements.txt
```

### 3. Configure environment variables

```powershell
copy .env.example .env
```

Edit `.env` and set the required variables (only `APP_MODE` is mandatory):

```dotenv
APP_MODE=production
# APP_ENV and DEBUG are optional, but in the sample .env they are present
APP_ENV=dev
PORT=8000
DEBUG=true
```

> Note: `APP_MODE` must be set to `production` for the application to run; otherwise `app.py` will raise at startup.

### 4. Run the application

```bash
python app.py
```

The application will print to the console:

```
Service started successfully
Port: 9123
```

### 5. Run the tests

Install `pytest` into the virtual environment and run tests:

```bash
# If you activated the environment
pip install pytest
pytest -q tests/
```

Or using the environment's python directly:

```bash
.\.venv\Scripts\python -m pip install pytest
.\.venv\Scripts\python -m pytest -q tests/
```

---

If you want to run tests using the provided `auto_test.py`, see the `auto_test.py` script in the repository which runs tests using the `.venv` Python interpreter and writes logs to `logs/test_run.log`.