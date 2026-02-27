"""
Meta API connector for publishing to Instagram and Facebook.
Uses the Facebook Graph API.
"""

import os
import time
import requests

# --- Configuration ---
META_ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN")
INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID")
FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
GRAPH_API_VERSION = "v19.0"
BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

def publish_to_instagram(local_path, media_url, caption):
    """
    Publishes to Instagram. IG prefers downloading from a public URL.
    """
    if not META_ACCESS_TOKEN or not INSTAGRAM_ACCOUNT_ID:
        print("Skipping Instagram: Missing credentials.")
        return False
        
    is_video = media_url.lower().endswith(('.mp4', '.mov'))
    
    # 1. Create Media Container
    container_url = f"{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media"
    payload = {
        "caption": caption,
        "access_token": META_ACCESS_TOKEN
    }
    
    if is_video:
        payload["media_type"] = "REELS"
        payload["video_url"] = media_url
    else:
        payload["image_url"] = media_url
        
    resp = requests.post(container_url, data=payload)
    if resp.status_code != 200:
        print(f"IG container creation failed: {resp.text}")
        return False
        
    container_id = resp.json().get("id")
    
    # 2. Wait for processing (only needed for video really)
    if is_video:
        status_url = f"{BASE_URL}/{container_id}"
        params = {
            "fields": "status_code",
            "access_token": META_ACCESS_TOKEN
        }
        max_attempts = 10
        for _ in range(max_attempts):
            s_resp = requests.get(status_url, params=params)
            status_code = s_resp.json().get("status_code")
            if status_code == "FINISHED":
                break
            elif status_code == "ERROR":
                print("IG Video processing failed.")
                return False
            time.sleep(5)
            
    # 3. Publish Media
    publish_url = f"{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    pub_payload = {
        "creation_id": container_id,
        "access_token": META_ACCESS_TOKEN
    }
    p_resp = requests.post(publish_url, data=pub_payload)
    
    if p_resp.status_code == 200:
        print(f"Successfully published to Instagram: {p_resp.json().get('id')}")
        return True
    else:
        print(f"IG publish failed: {p_resp.text}")
        return False

def publish_to_facebook(local_path, media_url, caption):
    """
    Publishes to Facebook Page.
    """
    if not META_ACCESS_TOKEN or not FB_PAGE_ID:
        print("Skipping Facebook: Missing credentials.")
        return False
        
    is_video = media_url.lower().endswith(('.mp4', '.mov'))
    
    if is_video:
        url = f"{BASE_URL}/{FB_PAGE_ID}/videos"
        payload = {
            "description": caption,
            "file_url": media_url,
            "access_token": META_ACCESS_TOKEN
        }
    else:
        url = f"{BASE_URL}/{FB_PAGE_ID}/photos"
        payload = {
            "message": caption,
            "url": media_url,
            "access_token": META_ACCESS_TOKEN
        }
        
    resp = requests.post(url, data=payload)
    if resp.status_code == 200:
        print(f"Successfully published to Facebook: {resp.json().get('id')}")
        return True
    else:
        print(f"Facebook publish failed: {resp.text}")
        return False

