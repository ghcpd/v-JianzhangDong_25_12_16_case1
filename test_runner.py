import sys
import os
import pathlib
import importlib.util
import inspect
import traceback

# ensure child processes spawned by tests see the required APP_MODE
os.environ.setdefault("APP_MODE", "production")

p = pathlib.Path(sys.argv[1])
if not p.exists():
    print(f"Test file not found: {p}")
    sys.exit(2)

spec = importlib.util.spec_from_file_location("m", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

failures = 0
for name, fn in inspect.getmembers(mod, inspect.isfunction):
    if name.startswith("test_"):
        try:
            fn()
            print(f"OK: {p.name}::{name}")
        except Exception:
            failures += 1
            print(f"FAIL: {p.name}::{name}")
            print(traceback.format_exc())

sys.exit(failures)
