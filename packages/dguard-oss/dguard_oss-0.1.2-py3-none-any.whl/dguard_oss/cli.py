import boto3
import sys
import os
from tqdm import tqdm
from rich.console import Console
console = Console()

from dguard_oss.config import load_config

def pprint(message):
    if "ERR" in message:
        console.print(message, style="bold red")
    elif "URL" in message or "FILE" in message:
        console.print(message, style="bold yellow underline")
    elif "Usage" in message:
        print(message)
    else:
        console.print(message, style="bold green")


# Progress bar callbacks
class Progress:
    def __init__(self, total_size):
        self._progress = tqdm(total=total_size, unit="B", unit_scale=True, unit_divisor=1024)

    def update(self, bytes_amount):
        self._progress.update(bytes_amount)

    def close(self):
        self._progress.close()


def upload(file_path, bucket_name, object_name, config_id):
    # 这里暂时没有使用 config_id，可根据实际需求修改
    s3_client = boto3.client(
        's3',
        endpoint_url=config_id['endpoint'],
        aws_access_key_id=config_id['access_key'],
        aws_secret_access_key=config_id['secret_key']
    )
    try:
        # 检查存储桶是否存在，如果不存在，尝试创建
        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except Exception:
            confirm = input(f"Bucket '{bucket_name}' does not exist. Create it? (yes/no): ").strip().lower()
            if confirm == "yes":
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                pprint("Operation aborted.")
                return

        file_size = os.path.getsize(file_path)
        progress = Progress(file_size)

        def upload_callback(bytes_amount):
            progress.update(bytes_amount)

        with open(file_path, 'rb') as file_data:
            s3_client.upload_fileobj(
                file_data,
                bucket_name,
                object_name,
                Callback=upload_callback
            )
        progress.close()

        pprint(f"[OSS] File '{file_path}' uploaded to bucket '{bucket_name}' as '{object_name}'.")
        pprint(f"[URL] {config_id['endpoint']}/{bucket_name}/{object_name}")
    except Exception as e:
        pprint(f"[OSS ERROR!] Upload failed: {e}")


def download(bucket_name, object_name, save_path, config_id):
    s3_client = boto3.client(
        's3',
        endpoint_url=config_id['endpoint'],
        aws_access_key_id=config_id['access_key'],
        aws_secret_access_key=config_id['secret_key']
    )

    try:
        # 获取对象信息以确定文件大小
        object_info = s3_client.head_object(Bucket=bucket_name, Key=object_name)
        file_size = object_info['ContentLength']
        progress = Progress(file_size)

        def download_callback(bytes_amount):
            progress.update(bytes_amount)

        with open(save_path, 'wb') as file_data:
            s3_client.download_fileobj(
                bucket_name,
                object_name,
                file_data,
                Callback=download_callback
            )
        progress.close()

        pprint(f"[OSS] File '{object_name}' from bucket '{bucket_name}' downloaded to '{save_path}'.")
    except Exception as e:
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
    print(help_text)


def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    command = sys.argv[1]
    config_id = load_config()

    # Extract --id option
    for arg in sys.argv:
        if arg.startswith("--id="):
            parts = arg.split("=", 1)
            if len(parts) == 2:
                config_id = load_config(parts[1])

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
    # config = load_config("config")
    # upload("/Users/zhaosheng/zhaosheng.sh", "temp", "zhaosheng.a",config)