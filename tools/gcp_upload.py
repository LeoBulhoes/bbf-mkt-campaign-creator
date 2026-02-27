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


def upload_reference(file_path, bucket_name=None, custom_name=None):
    """
    Upload a file to GCP Cloud Storage and return the public URL.

    Args:
        file_path: Path to the local file
        bucket_name: Optional bucket name override (defaults to config)
        custom_name: Optional destination blob name. 
                     If provided and starts with 'references/' or 'ads/', it will be used as is.
                     Otherwise it will be placed in 'references/'.

    Returns:
        str: The hosted download URL
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
        if custom_name:
            blob_name = custom_name
            if not (blob_name.startswith('references/') or blob_name.startswith('ads/')):
                blob_name = f"references/{blob_name}"
            # Ensure extension matches
            if not blob_name.endswith(ext):
                blob_name += ext
        else:
            blob_name = f"references/{uuid.uuid4().hex}{ext}"

        blob = bucket.blob(blob_name)
        blob.upload_from_filename(str(file_path))

        # Ensure the blob is public (if bucket is not uniformly uniform open)
        try:
            blob.make_public()
        except Exception as e:
            pass

        file_url = blob.public_url
        print_status(f"Upload successful: {file_url}", "OK")
        return file_url

    except Exception as e:
        raise Exception(f"GCP upload failed: {e}")


def upload_references(file_paths, bucket_name=None):
    """
    Upload multiple reference files and return their hosted URLs.
    Uses the original filename as the GCS blob name (e.g., references/mug_15oz_front.jpg).
    """
    urls = []
    for path in file_paths:
        filename = Path(path).name
        url = upload_reference(path, bucket_name, custom_name=f"references/{filename}")
        urls.append(url)
    return urls
def check_blob_exists(blob_name, bucket_name=None):
    """
    Check if a blob exists in the GCS bucket.
    
    Args:
        blob_name: Name of the blob/file in GCS (e.g., 'ads/product_ad.jpg')
        bucket_name: Optional bucket name override
        
    Returns:
        str: The public URL if it exists, None otherwise.
    """
    bucket_name = bucket_name or config.GCP_BUCKET_NAME
    if not bucket_name:
        return None
        
    try:
        client = get_storage_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        if blob.exists():
            return blob.public_url
        return None
    except Exception as e:
        print_status(f"Error checking GCS blob existence: {e}", "!!")
        return None
