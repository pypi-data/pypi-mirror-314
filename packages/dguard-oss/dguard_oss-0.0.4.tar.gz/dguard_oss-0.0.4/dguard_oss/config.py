import os
import json

from rich.console import Console
console = Console()

def print(message):
    if "ERR" in message:
        console.print(message, style="bold red")
    else:
        console.print(message, style="bold green")


CONFIG_DIR = os.path.expanduser("~/.dguard_oss")
DEFAULT_ID = "config"

# Ensure the configuration directory exists
def ensure_config_dir():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

# Load a configuration file based on the ID
def load_config(config_id=DEFAULT_ID):
    ensure_config_dir()
    config_path = os.path.join(CONFIG_DIR, f"{config_id}.json")

    if not os.path.exists(config_path):
        # try to find in /opt/.dguard_oss
        config_path_new = os.path.join("/opt/.dguard_oss", f"{config_id}.json")
        if os.path.exists(config_path_new):
            config_path = config_path_new
        else:
            print(f"[OSS ERROR!] Configuration file '{config_path}' does not exist.")
            create_new_config(config_path)

    with open(config_path, 'r') as f:
        config = json.load(f)
        # print(f"Loaded configuration for ID '{config_id}': {config}")
        return config

# Create a new configuration file

def create_new_config(config_path):
    print("Creating a new configuration file.")
    endpoint = input("Enter MinIO endpoint (e.g., play.min.io:9000): ")
    access_key = input("Enter MinIO access key: ")
    secret_key = input("Enter MinIO secret key: ")
    secure = input("Use HTTPS? (yes/no): ").strip().lower() == "yes"

    config = {
        "endpoint": endpoint,
        "access_key": access_key,
        "secret_key": secret_key,
        "secure": secure
    }

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
        print(f"Configuration saved to '{config_path}'.")


def create_new_config_cli():
    ensure_config_dir()
    config_id = input("Enter a configuration ID: ")
    config_path = os.path.join(CONFIG_DIR, f"{config_id}.json")
    create_new_config(config_path)

def check_config_cli():
    ensure_config_dir()
    config_id = input("Enter a configuration ID: ")
    config_path = os.path.join(CONFIG_DIR, f"{config_id}.json")
    a = load_config(config_id)
    print(a)

    