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
```
copy .env.example .env
```

Edit .env and set the following values:
```
APP_ENV=dev
PORT=8000
DEBUG=true
```

### 4. Run the application
```
python main.py
```

### 5. Verify the service
Open your browser and visit:
http://localhost:8000

If the page loads successfully, the service has started correctly.
