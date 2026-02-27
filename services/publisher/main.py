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
            
            # Use 'Generated Video 1' or 'Generated Image 1' as the media
            # If masked versions exist, prioritize those?
            media_att = fields.get("Masked Video 1") or fields.get("Generated Video 1") or \
                        fields.get("Masked Image 1") or fields.get("Generated Image 1")
                        
            if not media_att or not isinstance(media_att, list):
                print(f"Skipping {ad_name}: No valid media attachment.")
                continue
                
            media_url = media_att[0].get("url")
            if not media_url:
                print(f"Skipping {ad_name}: No media URL found.")
                continue
                
            # Download to temp file
            ext = media_url.split(".")[-1][:4] if "." in media_url else "tmp"
            # Cleanup URL parameters if they exist
            ext = ext.split("?")[0]
            local_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.{ext}")
            
            if not download_media(media_url, local_path):
                continue
                
            print(f"Publishing {ad_name} across platforms...")
            
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
        
        html = f"""
        <html>
            <body style="font-family: sans-serif; padding: 2rem;">
                <h1 style="color: green;">TikTok Authorization Successful!</h1>
                <p>Add these values directly to your <code>env.dev</code> and GCP Secret Manager:</p>
                <h3>TIKTOK_ACCESS_TOKEN</h3>
                <pre style="background:#eee;padding:10px;border-radius:4px;word-break: break-all;">{access_token}</pre>
                
                <h3>TIKTOK_REFRESH_TOKEN (Save this! It will let you refresh the token after {expires_in} seconds)</h3>
                <pre style="background:#eee;padding:10px;border-radius:4px;word-break: break-all;">{refresh_token}</pre>
                
                <p>Once you copy these to your `.env` (or GCP Secrets), you can close this window!</p>
            </body>
        </html>
        """
        return html, 200
        
    except Exception as e:
        return f"<h1>Server Error During Token Exchange</h1><p>{str(e)}</p>", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
