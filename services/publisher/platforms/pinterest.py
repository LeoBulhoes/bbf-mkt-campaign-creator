"""
Pinterest API connector.
"""

import os
import requests

PINTEREST_ACCESS_TOKEN = os.environ.get("PINTEREST_ACCESS_TOKEN")
PINTEREST_BOARD_ID = os.environ.get("PINTEREST_BOARD_ID")

def publish_to_pinterest(local_path, media_url, caption):
    """
    Publishes to a Pinterest Board.
    For this initial version, we support creating Pins from image URLs.
    Video requires a complex multi-step upload process which can be added later if needed.
    """
    if not PINTEREST_ACCESS_TOKEN or not PINTEREST_BOARD_ID:
        print("Skipping Pinterest: Missing credentials.")
        return False
        
    is_video = media_url.lower().endswith(('.mp4', '.mov'))
    if is_video:
        print("Skipping Pinterest: Video pins require multi-step upload (Not Implemented).")
        return False
        
    url = "https://api.pinterest.com/v5/pins"
    
    headers = {
        "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Extract a title from the caption (first line or first 50 chars)
    title = caption.split('\n')[0][:100] if caption else "Generated Pin"
    
    payload = {
        "board_id": PINTEREST_BOARD_ID,
        "media_source": {
            "source_type": "image_url",
            "url": media_url
        },
        "title": title,
        "description": caption
    }
    
    resp = requests.post(url, headers=headers, json=payload)
    
    if resp.status_code in (200, 201):
        print(f"Successfully published to Pinterest: {resp.json().get('id')}")
        return True
    else:
        print(f"Pinterest publish API failed: {resp.text}")
        return False
