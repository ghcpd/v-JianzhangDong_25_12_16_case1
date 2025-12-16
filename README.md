# Project Deployment Guide

## Overview
This is a Python service application that requires configuration and environment setup to run successfully.

## Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

## Setup Instructions

### 1. Create Virtual Environment
Create a clean Python virtual environment:
```bash
python -m venv .venv
```

Activate the virtual environment:

**On Windows:**
```bash
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### 2. Install Dependencies
Once the virtual environment is activated, install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Set the required environment variable:
```bash
# On Windows (PowerShell)
$env:APP_MODE = "production"

# On Windows (Command Prompt)
set APP_MODE=production

# On macOS/Linux
export APP_MODE=production
```

### 4. Verify Configuration
The service requires:
- **APP_MODE**: Must be set to "production"
- **settings.yaml**: Must exist in the project root
- **Port**: Service will run on port 9123 (configured in settings.yaml)

### 5. Run the Service
Start the service:
```bash
python app.py
```

Expected output:
```
Service started successfully
Port: 9123
```

## Running Tests
To execute all test cases, use the auto_test.py script:
```bash
python auto_test.py
```

This will:
- Start the application
- Run all tests in the `tests/` folder
- Log all results to `logs/test_run.log`

## Project Structure
```
.
├── app.py              # Main application entry point
├── config.py           # Configuration loader
├── settings.yaml       # Application configuration
├── requirements.txt    # Python dependencies
├── tests/              # Test suite
│   ├── case_1.py      # Test: app starts successfully
│   ├── case_2.py      # Test: output contains port
│   └── case_3.py      # Test: correct port is displayed
├── auto_test.py        # Automated test runner
├── logs/               # Test execution logs
└── .venv/             # Virtual environment (auto-created)
```

## Dependencies
- **PyYAML** (>= 6.0.2): For YAML configuration parsing

## Troubleshooting

### Error: "APP_MODE environment variable is required"
Ensure you've set the APP_MODE environment variable to "production" before running the application.

### Error: "settings.yaml not found"
Make sure settings.yaml exists in the project root directory.

### Error: "Port must be an integer"
Verify that the port value in settings.yaml is a valid integer.

## Notes
- The application validates that APP_MODE is set to "production" before starting
- The service uses PyYAML to parse the settings.yaml configuration file
- All tests must pass before the application is considered ready for deployment
