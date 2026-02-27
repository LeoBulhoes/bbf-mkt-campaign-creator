"""
Airtable synchronization specifically for the Publisher.
Reads ready records, downloads GCS media, and updates status to Published.
"""

import os
import requests
from google.cloud import storage

# --- Configuration ---
# These must be set in the Cloud Run environment variables or Secret Manager
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.environ.get("AIRTABLE_TABLE_NAME", "Content")
GCP_BUCKET_NAME = os.environ.get("GCP_BUCKET_NAME", "bluebullfly-assets")

def _headers():
    return {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json",
    }

def _table_url():
    return f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

def get_ready_assets():
    """
    Fetch records that are 'Approved' and not yet 'Published'.
    We assume a structure where either 'Image Status' = 'Approved' or 'Video Status' = 'Approved',
    and a new potential tag or status indicates it hasn't been published yet.
    For this initial logic, we look for {Video Status} = 'Approved' and {Publisher Status} = empty.
    """
    formula = "AND({Video Status} = 'Approved', {Publisher Status} = BLANK())"
    
    records = []
    offset = None
    
    while True:
        params = {"filterByFormula": formula}
        if offset:
            params["offset"] = offset
            
        resp = requests.get(_table_url(), headers=_headers(), params=params)
        if resp.status_code != 200:
            print(f"Error fetching from Airtable: {resp.text}")
            break
            
        data = resp.json()
        records.extend(data.get("records", []))
        
        offset = data.get("offset")
        if not offset:
            break
            
    return records

def mark_as_published(record_id):
    """
    Update a record to mark it as published.
    """
    url = f"{_table_url()}/{record_id}"
    fields = {
        "Publisher Status": "Published"
    }
    resp = requests.patch(url, headers=_headers(), json={"fields": fields})
    if resp.status_code != 200:
        print(f"Failed to update record {record_id}: {resp.text}")
        return False
    return True

def download_media(url, local_dest_path):
    """
    Downloads media from a public URL to a local path.
    Airtable provides public URLs for its attachments.
    """
    try:
        os.makedirs(os.path.dirname(local_dest_path), exist_ok=True)
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        
        with open(local_dest_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"Downloaded {url} to {local_dest_path}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

