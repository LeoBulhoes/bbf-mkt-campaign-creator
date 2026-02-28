import os
import tempfile
import uuid
import subprocess
import requests
from google.cloud import storage

# Load environment variables manually
env_path = os.path.join(os.path.dirname(__file__), '../../.env.dev')
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            if '=' in line:
                key, val = line.split('=', 1)
                os.environ[key] = val

from platforms.tiktok import publish_to_tiktok

def download_file(url, local_path):
    print(f"Downloading {url}...")
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(local_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return local_path

def upload_to_gcs(local_path, destination_blob_name):
    print(f"Uploading {local_path} to GCS...")
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.environ.get("GCP_BUCKET_NAME", "bluebullfly"))
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_path)
    # Make sure it's publicly readable?
    # Actually just accessing the URL might require MakePublic, but let's assume bucket is public
    url = f"https://storage.googleapis.com/{bucket.name}/{destination_blob_name}"
    print(f"Uploaded to {url}")
    return url

def create_video_with_audio(image_path, audio_path, output_path):
    print(f"Generating video from {image_path} and {audio_path}...")
    # Creates a 10s video looping the image with the audio track
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", "10", # 10 seconds
        output_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

def run_multi_post_test():
    image_urls = [
        "https://api.bluebullfly.com/assets/ads/cap_blue_front_ad_masked.jpg",
        "https://api.bluebullfly.com/assets/ads/hoodie_pink_front_ad_masked.jpg",
        "https://api.bluebullfly.com/assets/ads/mug_15oz_front_ad_masked.jpg"
    ]
    audio_url = "https://storage.googleapis.com/bluebullfly/songs/Bluebullfly_Fun.mp3"
    
    tmp_dir = tempfile.gettempdir()
    audio_path = download_file(audio_url, os.path.join(tmp_dir, "song.mp3"))
    
    # 1. Post independent videos
    for idx, img_url in enumerate(image_urls):
        # We need the real GCS URL just to download it locally to ffmpeg
        real_gcs_img_url = img_url.replace("https://api.bluebullfly.com/assets/", "https://storage.googleapis.com/bluebullfly/")
        img_path = download_file(real_gcs_img_url, os.path.join(tmp_dir, f"img_{idx}.jpg"))
        vid_path = os.path.join(tmp_dir, f"vid_{idx}.mp4")
        create_video_with_audio(img_path, audio_path, vid_path)
        
        # Uploading back to GCS gives us the base storage URL
        gcs_vid_url = upload_to_gcs(vid_path, f"tmp/vid_{uuid.uuid4().hex[:8]}.mp4")
        # Swap it instantly to our verified Proxy Domain before handing it to TikTok
        proxy_vid_url = gcs_vid_url.replace("https://storage.googleapis.com/bluebullfly/", "https://api.bluebullfly.com/assets/")
        print(f"Submitting Proxy URL to TikTok: {proxy_vid_url}")
        
        caption = f"Product Test {idx+1} ✨ #Sandbox"
        print(f"--- Attempting to publish TikTok Video {idx+1} ---")
        res = publish_to_tiktok(vid_path, proxy_vid_url, caption)
        print(f"Video {idx+1} Success: {res}\n")

    # 2. Post the photo carousel
    print("--- Attempting to publish TikTok Photo Carousel ---")
    caption_carousel = "Our Collection! ✨ #Sandbox"
    # Note: No audio possible here, TikTok will auto-assign
    res_carousel = publish_to_tiktok(None, image_urls, caption_carousel)
    print(f"Carousel Success: {res_carousel}\n")

if __name__ == "__main__":
    run_multi_post_test()
