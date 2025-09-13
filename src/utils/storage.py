import os, json, base64
from google.cloud import storage
from decouple import config


BUCKET_NAME = "cvmaker_files"


def get_storage_client() -> storage.Client:
    creds_json = base64.b64decode(config("GCP_CREDENTIALS")).decode("utf-8")
    creds_dict = json.loads(creds_json)

    client = storage.Client.from_service_account_info(creds_dict)

    return client


def upload_to_bucket(file_path: str, destination_blob_name: str) -> str:
    client = get_storage_client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(file_path, content_type="application/pdf")

    return blob.public_url
