"""
GCP file upload module.
Uploads reference product images to Google Cloud Storage.
"""

import os
from pathlib import Path
from google.cloud import storage
import uuid

from . import config
from .utils import print_status


def get_storage_client():
    """Get an authenticated GCS client."""
    return storage.Client()


def upload_reference(file_path, bucket_name=None):
    """
    Upload a file to GCP Cloud Storage and return the public URL.

    Args:
        file_path: Path to the local file
        bucket_name: Optional bucket name override (defaults to config)

    Returns:
        str: The hosted download URL

    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If upload fails
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    bucket_name = bucket_name or config.GCP_BUCKET_NAME
    if not bucket_name:
        raise ValueError("GCP_BUCKET_NAME is required in .env")

    print_status(f"Uploading to GCP ({bucket_name}): {file_path.name}")

    try:
        client = get_storage_client()
        bucket = client.bucket(bucket_name)

        # Generate a unique destination blob name
        ext = file_path.suffix
        blob_name = f"references/{uuid.uuid4().hex}{ext}"

        blob = bucket.blob(blob_name)
        blob.upload_from_filename(str(file_path))

        # Ensure the blob is public (if bucket is not uniformly uniform open)
        try:
            blob.make_public()
        except Exception as e:
            # Might fail if Uniform Bucket-Level Access is enforced, which is fine
            # as long as the bucket itself is public
            pass

        file_url = blob.public_url
        print_status(f"Upload successful: {file_url}", "OK")
        return file_url

    except Exception as e:
        raise Exception(f"GCP upload failed: {e}")


def upload_references(file_paths, bucket_name=None):
    """
    Upload multiple reference files and return their hosted URLs.

    Args:
        file_paths: List of local file paths
        bucket_name: Optional bucket name override

    Returns:
        list[str]: List of hosted URLs
    """
    urls = []
    for path in file_paths:
        url = upload_reference(path, bucket_name)
        urls.append(url)
    return urls
