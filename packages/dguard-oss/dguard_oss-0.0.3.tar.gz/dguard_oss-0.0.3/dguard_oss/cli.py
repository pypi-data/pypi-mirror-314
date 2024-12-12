import sys
import os
from tqdm import tqdm
from minio import Minio
from minio.error import S3Error
from dguard_oss.config import load_config, DEFAULT_ID
from rich.console import Console
console = Console()

def pprint(message):
    if "ERR" in message:
        console.pprint(message, style="bold red")
    elif "URL" in message or "FILE" in message:
        console.pprint(message, style="bold yellow underline")
    elif "Usage" in message:
        print(message)
    else:
        console.pprint(message, style="bold green")

# Progress bar callbacks
class Progress:
    def __init__(self, total_size):
        self._progress = tqdm(total=total_size, unit="B", unit_scale=True, unit_divisor=1024)

    def update(self, bytes_amount):
        self._progress.update(bytes_amount)

    def close(self):
        self._progress.close()

    def set_meta(self, object_name, total_length):
        self._progress.set_description_str(object_name)
        self._progress.total = total_length


def upload(file_path, bucket_name, object_name, config_id):
    config = load_config(config_id)
    client = Minio(
        config['endpoint'],
        config['access_key'],
        config['secret_key'],
        secure=config['secure']
    )
    try:
        if not client.bucket_exists(bucket_name):
            confirm = input(f"Bucket '{bucket_name}' does not exist. Create it? (yes/no): ").strip().lower()
            if confirm == "yes":
                client.make_bucket(bucket_name)
            else:
                pprint("Operation aborted.")
                return

        file_size = os.path.getsize(file_path)
        progress = Progress(file_size)

        with open(file_path, 'rb') as file_data:
            client.put_object(
                bucket_name,
                object_name,
                file_data,
                length=file_size,
                progress=progress
            )
        progress.close()

        pprint(f"[OSS] File '{file_path}' uploaded to bucket '{bucket_name}' as '{object_name}'.")
        pprint(f"[URL] {config['endpoint']}/{bucket_name}/{object_name}")
    except S3Error as e:
        pprint(f"[OSS ERROR!] Upload failed: {e}")


def download(bucket_name, object_name, save_path, config_id):
    config = load_config(config_id)
    client = Minio(
        config['endpoint'],
        config['access_key'],
        config['secret_key'],
        secure=config['secure']
    )

    try:
        stat = client.stat_object(bucket_name, object_name)
        file_size = stat.size
        progress = Progress(file_size)

        with client.get_object(bucket_name, object_name) as response_data:
            with open(save_path, 'wb') as file_data:
                for data in response_data.stream(1024 * 1024):
                    file_data.write(data)
                    progress.update(len(data))
        progress.close()

        pprint(f"[OSS] File '{object_name}' from bucket '{bucket_name}' downloaded to '{save_path}'.")
    except S3Error as e:
        pprint(f"[OSS ERROR!] Download failed: {e}")


def show_help():
    help_text = """
Usage:
  oss upload <file_path> [bucket] [object_name] [--id=<config_id>]
  oss download [bucket] <object_name> <save_path> [--id=<config_id>]
  oss help
  oss-config
  oss-config-new

Options:
  [--id=<config_id>]  Specify configuration ID. Defaults to 'config'.
  * oss-config: Display the configuration for a given ID.
  * oss-config-new: Create a new configuration file.
"""
    pprint(help_text)


def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    command = sys.argv[1]
    config_id = DEFAULT_ID

    # Extract --id option
    for arg in sys.argv:
        if arg.startswith("--id="):
            config_id = arg.split("=", 1)[1]

    if command == 'upload':
        if len(sys.argv) < 4:
            pprint("Error: Invalid arguments for 'upload'.")
            show_help()
            sys.exit(1)

        file_path = sys.argv[2]
        bucket_name = sys.argv[3] if len(sys.argv) > 3 else "temp"
        object_name = sys.argv[4] if len(sys.argv) > 4 else os.path.basename(file_path)
        upload(file_path, bucket_name, object_name, config_id)

    elif command == 'download':
        if len(sys.argv) < 4:
            pprint("Error: Invalid arguments for 'download'.")
            show_help()
            sys.exit(1)

        bucket_name = sys.argv[2]
        object_name = sys.argv[3]
        save_path = sys.argv[4]
        download(bucket_name, object_name, save_path, config_id)

    elif command == 'help':
        show_help()

    else:
        pprint(f"Unknown command: {command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()