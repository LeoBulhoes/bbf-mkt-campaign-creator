"""
YouTube Data API v3 connector (Shorts uploads).
"""

import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def publish_to_youtube(local_path, media_url, caption):
    """
    Uploads a video to YouTube Shorts.
    """
    if not local_path or not os.path.exists(local_path):
        print("Skipping YouTube: Valid local file required for upload.")
        return False
        
    is_video = local_path.lower().endswith(('.mp4', '.mov'))
    if not is_video:
        print("Skipping YouTube: Only video publishing is supported.")
        return False

    try:
        # Assumes the Cloud Run service account has proper scopes/delegation 
        # OR Application Default Credentials are set with YouTube scopes
        credentials, project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/youtube.upload"]
        )
        youtube = build("youtube", "v3", credentials=credentials)
        
        # Format for Shorts: Add #Shorts to title/description if not present
        title = caption.split('\n')[0][:90] if caption else "UGC Ad"
        if "#shorts" not in title.lower():
            title += " #Shorts"
            
        desc = caption if caption else ""
        if "#shorts" not in desc.lower():
            desc += "\n#Shorts"

        body = {
            "snippet": {
                "title": title,
                "description": desc,
                "tags": ["shorts", "ugc", "marketing"],
                "categoryId": "22" # 22 = People & Blogs, change as needed
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(local_path, chunksize=-1, resumable=True)

        print("Initiating YouTube upload...")
        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")

        print(f"Successfully published to YouTube: {response.get('id')}")
        return True

    except Exception as e:
        print(f"YouTube publish API failed: {e}")
        return False
