"""
TikTok Content Posting API connector.
"""

import os
import requests

TIKTOK_ACCESS_TOKEN = os.environ.get("TIKTOK_ACCESS_TOKEN")
TIKTOK_REFRESH_TOKEN = os.environ.get("TIKTOK_REFRESH_TOKEN")
TIKTOK_CLIENT_KEY = os.environ.get("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = os.environ.get("TIKTOK_CLIENT_SECRET")

def get_fresh_access_token():
    """
    Exchanges the long-lived refresh token for a new 24-hour access token.
    """
    if not all([TIKTOK_REFRESH_TOKEN, TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET]):
        print("Missing TikTok credentials for token refresh.")
        return None
        
    url = "https://open.tiktokapis.com/v2/oauth/token/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache"
    }
    payload = {
        "client_key": TIKTOK_CLIENT_KEY,
        "client_secret": TIKTOK_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": TIKTOK_REFRESH_TOKEN
    }
    
    try:
        resp = requests.post(url, headers=headers, data=payload)
        data = resp.json()
        if data.get("access_token"):
            return data.get("access_token")
        else:
            print(f"Failed to refresh TikTok token: {data}")
            return None
    except Exception as e:
        print(f"Error refreshing TikTok token: {e}")
        return None

def publish_to_tiktok(local_path, media_url, caption):
    """
    Publishes to TikTok using the Content Posting API (PULL_FROM_URL).
    Supports either a single video OR a list of image URLs (photo carousel).
    media_url: A string (video URL) OR a list of strings (image URLs).
    """
    access_token = TIKTOK_ACCESS_TOKEN or get_fresh_access_token()
    
    if not access_token:
        print("Skipping TikTok: Missing access token and could not refresh.")
        return False
        
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8"
    }

    # Handle Photo Carousel (List of URLs)
    if isinstance(media_url, list):
        if not media_url:
            print("Skipping TikTok: Empty image list provided for carousel.")
            return False
            
        print(f"Preparing TikTok Photo Carousel with {len(media_url)} images.")
        url = "https://open.tiktokapis.com/v2/post/publish/content/init/"
        
        payload = {
            "post_info": {
                "title": caption,
                "privacy_level": "SELF_ONLY",
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "photo_images": media_url
            },
            "post_mode": "DIRECT_POST",
            "media_type": "PHOTO"
        }
        
    # Handle Video (Single String URL)
    else:
        is_video = media_url.lower().endswith(('.mp4', '.mov'))
        if not is_video:
            print("Skipping TikTok: Media is not a video and not a list of images.")
            return False
            
        print("Preparing TikTok Video publish.")
        url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
        
        payload = {
            "post_info": {
                "title": caption,
                "privacy_level": "SELF_ONLY",
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
