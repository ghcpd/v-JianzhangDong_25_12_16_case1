#!/usr/bin/env python
"""
Auto test runner that starts the project and executes all test scripts.
Logs all results to logs/test_run.log
"""

import os
import sys
import subprocess
import logging
import importlib.util
from pathlib import Path
from datetime import datetime

# Ensure logs directory exists
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure logging
log_file = logs_dir / "test_run.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def set_environment_variables():
    """Set required environment variables for the application."""
    logger.info("Setting environment variables...")
    os.environ["APP_MODE"] = "production"
    logger.info("APP_MODE set to 'production'")


def start_project():
    """Start the project to verify it runs without errors."""
    logger.info("=" * 60)
    logger.info("Starting the project...")
    logger.info("=" * 60)
    
    try:
        result = subprocess.run(
            [sys.executable, "app.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        logger.info("Project Output:")
        logger.info(result.stdout)
        
        if result.returncode != 0:
            logger.error("Project startup failed!")
            logger.error(result.stderr)
            return False
        
        logger.info("Project started successfully!")
        return True
    
    except subprocess.TimeoutExpired:
        logger.warning("Project startup timed out (expected for long-running services)")
        return True
    except Exception as e:
        logger.error(f"Error starting project: {e}")
        return False


def run_tests():
    """Execute all test scripts in the tests/ folder."""
    logger.info("=" * 60)
    logger.info("Running test suite...")
    logger.info("=" * 60)
    
    tests_dir = Path("tests")
    if not tests_dir.exists():
        logger.error("tests/ directory not found")
        return False
    
    test_files = sorted(tests_dir.glob("case_*.py"))
    
    if not test_files:
        logger.warning("No test files found in tests/ directory")
        return False
    
    all_passed = True
    
    for test_file in test_files:
        logger.info(f"\nExecuting: {test_file.name}")
        logger.info("-" * 40)
        
        try:
            # Run the test module directly by importing and executing test functions
            spec = __import__('importlib.util').util.spec_from_file_location("test_module", test_file)
            module = __import__('importlib.util').util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find and execute all test functions
            test_functions = [func for func in dir(module) if func.startswith('test_')]
            
            if not test_functions:
                logger.warning(f"No test functions found in {test_file.name}")
                continue
            
            for test_func_name in test_functions:
                test_func = getattr(module, test_func_name)
                logger.info(f"Running {test_func_name}...")
                try:
                    test_func()
                    logger.info(f"  [PASSED] {test_func_name}")
                except AssertionError as e:
                    logger.error(f"  [FAILED] {test_func_name}: {e}")
                    all_passed = False
                except Exception as e:
                    logger.error(f"  [ERROR] {test_func_name}: {e}")
                    all_passed = False
            
            logger.info(f"Test file {test_file.name} completed")
        
        except Exception as e:
            logger.error(f"Error loading test file {test_file.name}: {e}")
            all_passed = False
    
    return all_passed


def main():
    """Main test runner."""
    logger.info("=" * 60)
    logger.info(f"Test Run Started: {datetime.now()}")
    logger.info("=" * 60)
    
    # Set environment variables
    set_environment_variables()
    
    # Start the project
    project_started = start_project()
    
    # Run tests
    tests_passed = run_tests()
    
    logger.info("=" * 60)
    logger.info("Test Run Summary")
    logger.info("=" * 60)
    project_status = "PASSED" if project_started else "FAILED"
    tests_status = "PASSED" if tests_passed else "FAILED"
    logger.info(f"Project Started: {project_status}")
    logger.info(f"All Tests: {tests_status}")
    logger.info(f"End Time: {datetime.now()}")
    logger.info("=" * 60)
    
    # Return appropriate exit code
    return 0 if (project_started and tests_passed) else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
