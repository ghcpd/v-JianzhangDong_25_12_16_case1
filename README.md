## Requirements

- Python 3.10+
- pip

---

## Quick Start

### 1. Create virtual environment

```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Configure environment variables

The application reads the `APP_MODE` environment variable (it **must** be set to `production`) and reads the port from `settings.yaml`.

# Windows (PowerShell)
$Env:APP_MODE = "production"

# macOS / Linux
export APP_MODE=production

Ensure `settings.yaml` contains the correct port (this project uses `9123` by default).

### 4. Run the application

Run the app with Python:

```
python app.py
```

### 5. Verify the service
The application prints startup confirmation to stdout. You should see output similar to:

```
Service started successfully
Port: 9123
```

(If you changed `settings.yaml` the port number will reflect that value.)

Manual tests can be run with `pytest`, e.g. `pytest tests/`. The project includes an automated runner `auto_test.py` that will install any missing test tools into `.venv/` and run the tests, saving logs to `logs/test_run.log`.