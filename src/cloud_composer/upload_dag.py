from pathlib import Path

from google.cloud import storage

COMPOSER_BUCKET = "ssb-tip-tutorials-automation-composer"
SOURCE_FILE_PATH = Path(__file__).with_name("god_dag.py")
DESTINATION_PATH = "dags/god_dag.py"


def upload_file(bucket_name: str, source_file_path: Path, destination_blob_name: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(str(source_file_path))
    print(f"File {source_file_path} uploaded to {destination_blob_name}.")


if __name__ == "__main__":
    upload_file(COMPOSER_BUCKET, SOURCE_FILE_PATH, DESTINATION_PATH)
