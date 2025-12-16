import os
import yaml

def load_config():
    if not os.path.exists("settings.yaml"):
        raise FileNotFoundError("settings.yaml not found")

    with open("settings.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    mode = os.getenv("APP_MODE")
    if not mode:
        raise EnvironmentError("APP_MODE environment variable is required")

    port = data.get("service", {}).get("port")
    if not isinstance(port, int):
        raise ValueError("Port must be an integer")

    return {
        "mode": mode,
        "port": port,
    }
