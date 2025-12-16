import sys
from config import load_config

def main():
    config = load_config()

    if config["mode"] != "production":
        raise RuntimeError(
            f"Invalid APP_MODE: {config['mode']} (must be 'production')"
        )

    print("Service started successfully")
    print(f"Port: {config['port']}")

if __name__ == "__main__":
    main()
