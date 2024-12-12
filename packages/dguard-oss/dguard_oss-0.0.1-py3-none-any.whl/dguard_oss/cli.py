# CLI changes for specifying config IDs
import sys
from minio import Minio
from minio.error import S3Error
from dguard_oss.config import load_config, DEFAULT_ID

# CLI tool

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
                print("Operation aborted.")
                return

        client.fput_object(bucket_name, object_name, file_path)
        print(f"File '{file_path}' uploaded to bucket '{bucket_name}' as '{object_name}'.")
        print(f"URL: {config['endpoint']}/{bucket_name}/{object_name}")
    except S3Error as e:
        print(f"Upload failed: {e}")


def download(bucket_name, object_name, save_path, config_id):
    config = load_config(config_id)
    client = Minio(
        config['endpoint'],
        config['access_key'],
        config['secret_key'],
        secure=config['secure']
    )
    try:
        client.fget_object(bucket_name, object_name, save_path)
        print(f"File '{object_name}' from bucket '{bucket_name}' downloaded to '{save_path}'.")
    except S3Error as e:
        print(f"Download failed: {e}")


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
    config_id = DEFAULT_ID

    # Extract --id option
    for arg in sys.argv:
        if arg.startswith("--id="):
            config_id = arg.split("=", 1)[1]

    if command == 'upload':
        if len(sys.argv) < 4:
            print("Error: Invalid arguments for 'upload'.")
            show_help()
            sys.exit(1)

        file_path = sys.argv[2]
        bucket_name = sys.argv[3] if len(sys.argv) > 3 else "temp"
        object_name = sys.argv[4] if len(sys.argv) > 4 else os.path.basename(file_path)
        upload(file_path, bucket_name, object_name, config_id)

    elif command == 'download':
        if len(sys.argv) < 4:
            print("Error: Invalid arguments for 'download'.")
            show_help()
            sys.exit(1)

        bucket_name = sys.argv[2] if len(sys.argv) > 2 else "temp"
        object_name = sys.argv[3]
        save_path = sys.argv[4]
        download(bucket_name, object_name, save_path, config_id)

    elif command == 'help':
        show_help()

    else:
        print(f"Unknown command: {command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
