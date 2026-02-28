"""
Main entry point for the Publishing API Connector.
Triggered via Cloud Scheduler. Evaluates 'Ready' assets in Airtable,
downloads them, and publishes to target platforms.
"""

from flask import Flask, request, jsonify
import os
import uuid
import tempfile

from airtable_sync import get_ready_assets, mark_as_published, download_media
from platforms.meta import publish_to_instagram, publish_to_facebook
from platforms.tiktok import publish_to_tiktok
from platforms.pinterest import publish_to_pinterest
from platforms.youtube import publish_to_youtube

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def run_publisher():
    """
    Cloud Run Job / Service entry point.
    """
    try:
        print("Fetching ready assets from Airtable...")
        assets = get_ready_assets()
        if not assets:
            print("No ready assets found.")
            return jsonify({"status": "success", "message": "No assets to publish"}), 200
            
        published_count = 0
            
        for asset in assets:
            record_id = asset["id"]
            fields = asset.get("fields", {})
            ad_name = fields.get("Ad Name", "untitled")
            caption = fields.get("Caption", "Default caption")
            
            media_att = fields.get("Masked Video 1") or fields.get("Generated Video 1")
            
            # If no video found, fallback to images for a photo carousel (currently only TikTok supports this in our integration)
            is_carousel = False
            if not media_att:
                media_att = fields.get("Masked Image 1") or fields.get("Generated Image 1")
                is_carousel = True
                
            if not media_att or not isinstance(media_att, list):
                print(f"Skipping {ad_name}: No valid media attachment.")
                continue
                
            # For videos, we take the first URL
            # For carousels, we take a list of all URLs
            if is_carousel:
                media_url = [att.get("url") for att in media_att if att.get("url")]
                local_path = None # We don't download local copies for carousels right now
            else:
                media_url = media_att[0].get("url")
                
                # Download to temp file
                ext = media_url.split(".")[-1][:4] if "." in media_url else "tmp"
                # Cleanup URL parameters if they exist
                ext = ext.split("?")[0]
                local_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.{ext}")
                
                if not download_media(media_url, local_path):
                    continue
                    
            print(f"Publishing {ad_name} across platforms...")
            
            if is_carousel:
                print("Detected image assets. Attempting to publish Photo Carousel to TikTok...")
                publish_to_tiktok(local_path, media_url, caption)
                # Currently skipping other platforms for photo carousels as their integrations expect video files
            else:
                publish_to_instagram(local_path, media_url, caption)
                publish_to_facebook(local_path, media_url, caption)
                publish_to_tiktok(local_path, media_url, caption)
                publish_to_pinterest(local_path, media_url, caption)
                publish_to_youtube(local_path, media_url, caption)
            
            print(f"Successfully published {ad_name}. Marking as published.")
            mark_as_published(record_id)
            published_count += 1
            
            # Cleanup temp file
            if os.path.exists(local_path):
                os.remove(local_path)
                
        return jsonify({
            "status": "success", 
            "message": f"Successfully published {published_count} assets."
        }), 200
        
    except Exception as e:
        print(f"Publisher error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/assets/<path:blob_name>", methods=["GET"])
def proxy_gcs_asset(blob_name):
    """
    Proxies media files from Google Cloud Storage.
    This masks the storage.googleapis.com domain with our own API domain,
    bypassing TikTok's strict 'url_ownership_unverified' sandbox restriction.
    """
    try:
        from google.cloud import storage
        from flask import Response
        import mimetypes
        
        bucket_name = os.environ.get("GCP_BUCKET_NAME", "bluebullfly")
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        if not blob.exists():
            return "Asset not found", 404
            
        def generate():
            # Download the blob in chunks completely in-memory and stream it to the client
            with blob.open("rb") as f:
                while chunk := f.read(8192):
                    yield chunk
                    
        # Guess the correct mimetype so TikTok parses it correctly
        mime_type, _ = mimetypes.guess_type(blob_name)
        if not mime_type:
            mime_type = "application/octet-stream"
            
        return Response(generate(), mimetype=mime_type)
        
    except Exception as e:
        print(f"GCS Proxy Error: {e}")
        return str(e), 500

@app.route("/tiktoktrY7FK0lCU5ICdE1F6sLQjhtuMwh3rJk.txt", methods=["GET"])
def tiktok_verify():
    """
    Route to serve the TikTok Domain Verification file.
    """
    return "tiktok-developers-site-verification=trY7FK0lCU5ICdE1F6sLQjhtuMwh3rJk", 200

@app.route("/tiktok/callback", methods=["GET"])
def tiktok_callback():
    """
    Handle the OAuth redirect callback from TikTok when creating the API app.
    TikTok will redirect to this URL with an authorization code.
    We will automatically exchange this code for an access token.
    """
    code = request.args.get("code")
    scopes = request.args.get("scopes")
    state = request.args.get("state")
    error = request.args.get("error")
    
    if error:
        return f"<h1>TikTok Authorization Failed</h1><p>Error: {error}</p>", 400
        
    if not code:
        return f"<h1>TikTok Authorization Failed</h1><p>No code provided.</p>", 400
        
    client_key = os.environ.get("TIKTOK_CLIENT_KEY")
    client_secret = os.environ.get("TIKTOK_CLIENT_SECRET")
    redirect_uri = os.environ.get("TIKTOK_REDIRECT_URI", "https://api.bluebullfly.com/tiktok/callback")
    
    if not client_key or not client_secret:
        return f"<h1>Configuration Error</h1><p>Missing TIKTOK_CLIENT_KEY or TIKTOK_CLIENT_SECRET in Cloud Run environment variables.</p>", 500
        
    # Exchange the code for an access token
    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    payload = {
        "client_key": client_key,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache"
    }
    
    import requests
    try:
        resp = requests.post(token_url, data=payload, headers=headers)
        data = resp.json()
        
        if data.get("error"):
            # Some errors might be nested inside 'error'
            err_msg = data.get("error_description", data.get("message", str(data)))
            return f"<h1>TikTok Token Exchange Failed</h1><p>{err_msg}</p><pre>{data}</pre>", 400
            
        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")
        expires_in = data.get("expires_in")
        
        # SECURE LOGGING: Print the tokens so they go to GCP Cloud Logging
        # Users must have GCP IAM permissions to view these tokens.
        print("\n" + "="*50)
        print(f"TIKTOK_ACCESS_TOKEN={access_token}")
        print(f"TIKTOK_REFRESH_TOKEN={refresh_token}")
        print("="*50 + "\n")
        
        html = f"""
        <html>
            <body style="font-family: sans-serif; padding: 2rem;">
                <h1 style="color: green;">TikTok Authorization Successful!</h1>
                <p>For security purposes, the tokens are not displayed on this page.</p>
                <p>Please check the <strong>Cloud Run Logs</strong> for the <code>publisher-api</code> service in your Google Cloud Console to retrieve the tokens.</p>
                <p><a href="https://console.cloud.google.com/logs/query?project={os.environ.get('GCP_PROJECT_ID', 'bluebullfly-5cc16')}">Click here to view your GCP Logs</a></p>
                <p>Once you copy them to your `.env` (or GCP Secrets), you can close this window!</p>
            </body>
        </html>
        """
        return html, 200
        
    except Exception as e:
        return f"<h1>Server Error During Token Exchange</h1><p>{str(e)}</p>", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
