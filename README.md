## Requirements

- Python 3.10+
- pip

---

## Quick Start

### 1. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Configure environment variables

Set the required environment variable:
```bash
set APP_MODE=production
```

### 4. Run the application

```bash
python app.py
```

The application will start and display output similar to:
```
Service started successfully
Port: 9123
```

### 5. Run tests

Execute the test suite:
```bash
python auto_test.py
```

Test results will be written to `logs/test_run.log`.