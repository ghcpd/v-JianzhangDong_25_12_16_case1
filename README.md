## Requirements

- Python 3.10+
- pip

---

## Quick Start

### 1. Create a clean virtual environment (recommended: .venv)

We use a project-local virtual environment named `.venv` in this repository. If a `.venv` folder already exists it is safe to delete and recreate it.

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
``` 
Windows (cmd.exe):
```cmd
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

Once the virtual environment is active install dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

Note: This project currently only requires `pyyaml` to load settings.

### 3. Required environment variable

This project does not use `.env.example` or APP_ENV/DEBUG. Instead it reads the port from `settings.yaml` and requires the environment variable `APP_MODE` to be set to `production` in order to start successfully.

Set it before running (PowerShell example):
```powershell
$env:APP_MODE = "production"
```
Or (cmd.exe):
```cmd
set APP_MODE=production
```

### 4. Run the application

Start the service with the correct entrypoint (the project uses `app.py`):

```bash
python app.py
```

Expected output:
```
Service started successfully
Port: 9123
```

### 5. Run the project's automated tests (and logging)

A convenience runner `auto_test.py` is included. It will:
 - start the application (with APP_MODE=production)
 - execute each test script found in the `tests/` folder using the Python interpreter from `.venv`
 - write a brief test summary to `logs/test_run.log` (the `logs/` directory will be created if necessary)

Run it with the `.venv` interpreter, for example (PowerShell):
```powershell
.\.venv\Scripts\python auto_test.py
```

If you prefer to run tests manually you can also use `python -m pytest` from an activated `.venv` (install pytest first if you need that).

If something fails, please check `logs/test_run.log` for details and ensure `APP_MODE` is set to `production` and `settings.yaml` contains a numeric `service.port` value.
