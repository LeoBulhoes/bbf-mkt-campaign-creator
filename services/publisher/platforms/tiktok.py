"""
TikTok Content Posting API connector.
"""

import os
import requests

TIKTOK_ACCESS_TOKEN = os.environ.get("TIKTOK_ACCESS_TOKEN")

def publish_to_tiktok(local_path, media_url, caption):
    """
    Publishes to TikTok using the Content Posting API (PULL_FROM_URL).
    Only supports videos.
    """
    if not TIKTOK_ACCESS_TOKEN:
        print("Skipping TikTok: Missing credentials.")
        return False
        
    is_video = media_url.lower().endswith(('.mp4', '.mov'))
    if not is_video:
        print("Skipping TikTok: Only video publishing is supported.")
        return False
        
    url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    
    headers = {
        "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    
    payload = {
        "post_info": {
            "title": caption,
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 1000
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "video_url": media_url
        }
    }
    
    resp = requests.post(url, headers=headers, json=payload)
    
    if resp.status_code == 200:
        data = resp.json()
        if data.get("error", {}).get("code") == "ok":
            print(f"Successfully initiated TikTok publish: {data.get('data', {}).get('publish_id')}")
            return True
        else:
            print(f"TikTok publish error in response: {data}")
            return False
    else:
        print(f"TikTok publish API failed: {resp.text}")
        return False
