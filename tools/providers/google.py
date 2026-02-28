"""
Google AI Studio provider — image generation (Nano Banana / Nano Banana Pro)
and video generation (Veo 3.1) via the Gemini API.

Image generation is SYNCHRONOUS (response contains base64 image data).
Video generation is ASYNCHRONOUS (returns operation ID, needs polling).

Generated assets are uploaded to Kie.ai hosting to get URLs for Airtable.
"""

import base64
import os
import time
import tempfile
import uuid
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from io import BytesIO
from PIL import Image

from .. import config
from ..utils import print_status
from ..gcp_upload import upload_reference

# Provider sync flags
image_IS_SYNC = True      # Images return immediately (no polling)
video_IS_SYNC = False     # Videos need polling

# --- Google model IDs ---
_IMAGE_MODELS = {
    "nano-banana": "gemini-2.5-flash-image",
    "nano-banana-pro": "gemini-3-pro-image-preview",
}

_VIDEO_MODELS = {
    "veo-3.1": "veo-3.1-generate-preview",
}

# --- API URLs ---
_GENERATE_CONTENT_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
_PREDICT_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:predictLongRunning"
_POLL_URL = "https://generativelanguage.googleapis.com/v1beta/{operation_name}"


def _headers():
    """Auth headers for Google AI Studio."""
    return {
        "x-goog-api-key": config.GOOGLE_AISTUDIO_API_KEY,
        "Content-Type": "application/json",
    }


def _encode_image_base64(file_path):
    """Read a local image file and return (base64_data, mime_type)."""
    path = Path(file_path)
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }
    mime_type = mime_map.get(path.suffix.lower(), "image/png")
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return data, mime_type


def _upload_base64_to_host(base64_data, filename="generated.png", custom_name=None, apply_mask=False):
    """
    Decode base64 image data, save to temp file, upload to GCP hosting.
    Also composites the Ad Mask if apply_mask is True and uploads the masked version.
    Returns a dict with 'original' and optionally 'masked' URLs.

    Args:
        base64_data: Base64-encoded image data
        filename: Temp file name for local save
        custom_name: Optional GCS blob name (passed to upload_reference)
        apply_mask: Whether to apply the Ad Mask overlay
    """
    tmp_path = os.path.join(tempfile.gettempdir(), filename)
    image_data = base64.b64decode(base64_data)
    with open(tmp_path, "wb") as f:
        f.write(image_data)
        
    urls = {}
    try:
        urls["original"] = upload_reference(tmp_path, custom_name=custom_name)
        
        if apply_mask:
            mask_path = os.path.join(config.PROJECT_ROOT, "references", "brands", "bluebullfly", "logo", "Ad Mask.png")
            if os.path.exists(mask_path):
                img = Image.open(BytesIO(image_data)).convert("RGBA")
                mask = Image.open(mask_path).convert("RGBA")
                
                # Resize mask to fit width of image if needed, or just overlay
                # The mask should be overlaid at the top-left
                mask_w, mask_h = mask.size
                img_w, img_h = img.size
                
                # Resize mask relatively if it's too big, or use it as is?
                # Usually we can just composite it directly. Let's make sure it fits
                if mask_w > img_w or mask_h > img_h:
                    mask.thumbnail((img_w, img_h), Image.Resampling.LANCZOS)
                
                img.alpha_composite(mask, (0, 0))
                
                masked_filename = "masked_" + filename
                masked_tmp_path = os.path.join(tempfile.gettempdir(), masked_filename)
                
                # Save as same format, dropping alpha if JPEG
                out_format = "JPEG" if filename.lower().endswith(('.jpg', '.jpeg')) else "PNG"
                if out_format == "JPEG":
                    img = img.convert("RGB")
                    
                img.save(masked_tmp_path, format=out_format)
                
                masked_custom_name = None
                if custom_name:
                    path_parts = custom_name.rsplit('.', 1)
                    masked_custom_name = f"{path_parts[0]}_masked.{path_parts[1]}" if len(path_parts) > 1 else f"{custom_name}_masked"
                
                urls["masked"] = upload_reference(masked_tmp_path, custom_name=masked_custom_name)
                os.remove(masked_tmp_path)
            else:
                print_status(f"Warning: Ad Mask not found at {mask_path}", "!!")
                
        return urls
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# ---------------------------------------------------------------------------
# Image Generation (Synchronous)
# ---------------------------------------------------------------------------

def submit_image(prompt, image_urls=None, aspect_ratio="9:16",
                 resolution="1K", model="nano-banana-pro", **kwargs):
    """
    Generate an image synchronously via Google AI Studio.

    Args:
        prompt: Image generation prompt
        image_urls: List of URLs for visual anchors (Product Consistency)
        aspect_ratio: Standard ratio string (e.g., "9:16")
        resolution: "1K", "2K", or "4K"
        model: "nano-banana" or "nano-banana-pro"

    Returns:
        dict: GenerationResult with status, result_url, task_id=None
    """
    google_model = _IMAGE_MODELS.get(model)
    if not google_model:
        raise ValueError(f"Google doesn't support image model: '{model}'")

    # Build parts: text prompt + anchor images as inline base64
    parts = [{"text": prompt}]

    # Handle URLs (Airtable/Hosted)
    if image_urls:
        for url in image_urls:
            try:
                ref_resp = requests.get(url, timeout=60)
                ref_resp.raise_for_status()
                b64 = base64.b64encode(ref_resp.content).decode("utf-8")
                mtype = ref_resp.headers.get("content-type", "image/jpeg")
                parts.append({
                    "inline_data": {"mime_type": mtype, "data": b64}
                })
            except Exception as e:
                print_status(f"Warning: Failed to download image URL {url[:40]}...: {e}", "!!")

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
        },
    }

    url = _GENERATE_CONTENT_URL.format(model=google_model)
    response = requests.post(url, headers=_headers(), json=payload, timeout=120)

    if response.status_code != 200:
        raise Exception(f"Google AI error {response.status_code}: {response.text[:500]}")

    result = response.json()

    # Extract base64 image from response candidates
    candidates = result.get("candidates", [])
    if not candidates:
        raise Exception(f"No candidates in Google AI response: {result}")

    resp_parts = candidates[0].get("content", {}).get("parts", [])
    # Build GCS destination name from ad_filename if provided
    ad_filename = kwargs.get("ad_filename")

    for part in resp_parts:
        if "inlineData" in part:
            b64_data = part["inlineData"]["data"]
            mime = part["inlineData"].get("mimeType", "image/png")
            ext = ".png" if "png" in mime else ".jpg"

            # Use product-variant-based name when available
            custom_name = None
            if ad_filename:
                custom_name = f"ads/{ad_filename}{ext}"

            hosted_urls = _upload_base64_to_host(
                b64_data, 
                f"google_gen{ext}", 
                custom_name=custom_name,
                apply_mask=True  # Apply brand mask to all images
            )
            return {
                "status": "success",
                "result_url": hosted_urls["original"],
                "masked_url": hosted_urls.get("masked"),
                "task_id": None,
            }

    raise Exception(f"No image data in Google AI response parts: {[list(p.keys()) for p in resp_parts]}")


def poll_image(task_id, **kwargs):
    """No-op — Google image generation is synchronous."""
    raise NotImplementedError("Google image generation is synchronous, no polling needed")


# ---------------------------------------------------------------------------
# Video Generation (Asynchronous — Veo 3.1)
# ---------------------------------------------------------------------------

_VIDEO_MODELS = {
    "veo-3.1": "veo-3.1-generate-preview",
}

def submit_video(prompt, image_urls=None, model="veo-3.1",
                 duration="8", aspect_ratio="9:16", resolution="720p", **kwargs):
    """
    Submit a video generation task to Google Veo 3.1.

    Args:
        prompt: Video prompt text
        image_urls: List of URLs. First is starting frame, rest are anchors.
        model: "veo-3.1"
        duration: "4", "6", or "8" seconds
        aspect_ratio: "9:16" or "16:9"
        resolution: "720p", "1080p", or "4k"

    Returns:
        str: operation_name for polling
    """
    google_model = _VIDEO_MODELS.get(model)
    if not google_model:
        raise ValueError(f"Google doesn't support video model: '{model}'")

    # Build instance
    instance = {"prompt": prompt}

    # Handle image list
    # Veo 3.1 image format: use bytesBase64Encoded (NOT inlineData) for REST API.
    # First image is the start frame (instances[0].image).
    # Additional images (referenceImages) are not currently available for this API plan.
    if image_urls:
        for i, url in enumerate(image_urls):
            try:
                resp = requests.get(url, timeout=60)
                resp.raise_for_status()
                b64 = base64.b64encode(resp.content).decode("utf-8")
                mtype = resp.headers.get("content-type", "image/jpeg").split(";")[0].strip()

                if i == 0:
                    # First image: starting frame in instances
                    instance["image"] = {"bytesBase64Encoded": b64, "mimeType": mtype}
                else:
                    # Skip additional images — referenceImages not available on this plan
                    print_status(f"Note: Skipping extra image {i} (referenceImages not available on this plan)", "!!")
            except Exception as e:
                print_status(f"Warning: Failed to download URL {url[:40]}...: {e}", "!!")

    # Veo 3.1 only accepts 4, 6, or 8 seconds
    valid_durations = [4, 6, 8]
    dur = int(duration)
    dur = min(valid_durations, key=lambda v: abs(v - dur))

    # image-to-video requires personGeneration=allow_adult and duration=8s
    # text-to-video uses allow_all so generated videos can include children in output
    has_image = "image" in instance
    if has_image:
        dur = 8

    payload = {
        "instances": [instance],
        "parameters": {
            "aspectRatio": aspect_ratio,
            "durationSeconds": int(duration),
            "sampleCount": 1,
            "personGeneration": "allow_adult" if has_image else "allow_all",
        },
    }

    import json
    print("\n--- VEO REQUEST PAYLOAD ---")
    print(json.dumps(payload, indent=2))
    print("---------------------------\n")

    url = _PREDICT_URL.format(model=google_model)
    response = requests.post(url, headers=_headers(), json=payload, timeout=120)

    if response.status_code != 200:
        raise Exception(f"Google Veo error {response.status_code}: {response.text[:500]}")

    result = response.json()
    operation_name = result.get("name")
    if not operation_name:
        raise Exception(f"No operation name in Veo response: {result}")

    return operation_name


def poll_video(operation_name, max_wait=600, poll_interval=10, quiet=False):
    """
    Poll a Google Veo operation until completion.
    Downloads the result video and uploads to a cloud hosting service.

    Args:
        operation_name: The operation name from submit_video
        max_wait: Maximum seconds to wait
        poll_interval: Seconds between checks
        quiet: Suppress status messages

    Returns:
        dict: GenerationResult with status, result_url, task_id
    """
    start_time = time.time()

    while time.time() - start_time < max_wait:
        url = _POLL_URL.format(operation_name=operation_name)
        response = requests.get(url, headers=_headers(), timeout=30)

        if response.status_code != 200:
            elapsed = int(time.time() - start_time)
            if not quiet:
                print_status(f"Poll returned {response.status_code}, retrying... ({elapsed}s)", "!!")
            time.sleep(poll_interval)
            continue

        result = response.json()

        if result.get("done"):
            # Check for error
            if "error" in result:
                error_msg = result["error"].get("message", str(result["error"]))
                raise Exception(f"Veo task failed: {error_msg}")

            # Extract video URI
            video_response = result.get("response", {}).get("generateVideoResponse", {})
            samples = video_response.get("generatedSamples", [])
            if not samples:
                raise Exception(f"No generated samples in Veo response: {result}")

            video_uri = samples[0].get("video", {}).get("uri")
            if not video_uri:
                raise Exception(f"No video URI in Veo response: {samples[0]}")

            # Download video (requires API key auth) and upload to GCS/Airtable
            hosted_urls = _download_and_host_video(video_uri, apply_mask=True)

            if not quiet:
                print_status("Veo task completed successfully!", "OK")

            return {
                "status": "success",
                "result_url": hosted_urls["original"],
                "masked_url": hosted_urls.get("masked"),
                "task_id": operation_name,
            }

        # Still processing
        elapsed = int(time.time() - start_time)
        mins, secs = divmod(elapsed, 60)
        if not quiet:
            print_status(f"Veo status: processing ({mins}m {secs}s elapsed)", "..")
        time.sleep(poll_interval)

    raise Exception(f"Veo timeout after {max_wait}s for operation: {operation_name}")


def _download_and_host_video(video_uri, apply_mask=False):
    """Download a Veo video, apply mask if requested (requires API key), and upload to GCP hosting."""
    import subprocess
    try:
        import imageio_ffmpeg
        has_ffmpeg = True
    except ImportError:
        has_ffmpeg = False
        
    tmp_path = os.path.join(tempfile.gettempdir(), f"veo_video_{uuid.uuid4().hex[:8]}.mp4")

    response = requests.get(video_uri, headers=_headers(), stream=True, timeout=120)
    response.raise_for_status()

    with open(tmp_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    urls = {}
    try:
        urls["original"] = upload_reference(tmp_path)
        
        if apply_mask:
            mask_path = os.path.join(config.PROJECT_ROOT, "references", "brands", "bluebullfly", "logo", "Ad Mask.png")
            if os.path.exists(mask_path) and has_ffmpeg:
                ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                masked_path = os.path.join(tempfile.gettempdir(), f"veo_masked_{uuid.uuid4().hex[:8]}.mp4")
                
                cmd = [
                    ffmpeg_exe, "-y",
                    "-i", tmp_path,
                    "-i", mask_path,
                    "-filter_complex", "[1:v][0:v]scale2ref[mask][main];[main][mask]overlay=0:0",
                    "-c:a", "copy",
                    masked_path
                ]
                
                try:
                    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    urls["masked"] = upload_reference(masked_path)
                except Exception as e:
                    print_status(f"Warning: Failed to mask video: {e}", "XX")
                finally:
                    if os.path.exists(masked_path):
                        os.remove(masked_path)
            elif not has_ffmpeg:
                print_status("Warning: imageio_ffmpeg not installed; skipping video mask", "!!")
            else:
                print_status(f"Warning: Ad Mask not found at {mask_path}", "!!")
                
        return urls
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def poll_tasks_parallel(operation_names, max_wait=600, poll_interval=10):
    """
    Poll multiple Google Veo operations concurrently.

    Args:
        operation_names: List of operation name strings
        max_wait: Max seconds to wait per operation
        poll_interval: Seconds between checks

    Returns:
        dict: operation_name → GenerationResult
    """
    if not operation_names:
        return {}

    total = len(operation_names)
    completed = []
    results = {}

    def _poll_one(op_name):
        result = poll_video(op_name, max_wait=max_wait,
                            poll_interval=poll_interval, quiet=True)
        completed.append(op_name)
        short = op_name.split("/")[-1][:12] if "/" in op_name else op_name[:12]
        print_status(f"Veo {short}... done ({len(completed)}/{total})", "OK")
        return result

    max_workers = min(total, 20)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_poll_one, name): name
            for name in operation_names
        }
        for future in as_completed(futures):
            name = futures[future]
            try:
                results[name] = future.result()
            except Exception as e:
                completed.append(name)
                short = name.split("/")[-1][:12] if "/" in name else name[:12]
                print_status(f"Veo {short}... failed: {e}", "XX")
                results[name] = {
                    "status": "error",
                    "task_id": name,
                    "error": str(e),
                }

    return results
