"""
Configuration loader for Creative Content Engine.
Loads API keys from references/.env and provides centralized constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from references/.env
PROJECT_ROOT = Path(__file__).parent.parent
ENV_PATH = PROJECT_ROOT / "references" / ".env"
load_dotenv(ENV_PATH)

# --- API Keys ---
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
GOOGLE_AISTUDIO_API_KEY = os.getenv("GOOGLE_AISTUDIO_API_KEY")
GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")

# --- WaveSpeed AI ---
WAVESPEED_API_KEY = os.getenv("WAVESPEED_API_KEY")
WAVESPEED_API_URL = "https://api.wavespeed.ai/api/v3"

# --- Airtable ---
AIRTABLE_API_URL = "https://api.airtable.com/v0"
AIRTABLE_TABLE_NAME = "Content"

# --- Cost Constants ---
IMAGE_COST = 0.04   # per Nano Banana image
VIDEO_COST = 0.50   # per Veo 3.1 video
WAVESPEED_VIDEO_COST = 0.30  # per Kling/Sora video via WaveSpeed (approximate)

# --- Per-model per-provider costs ---
COSTS = {
    # Image models
    ("nano-banana", "google"): 0.04,
    ("nano-banana-pro", "google"): 0.13,
    ("gpt-image-1.5", "wavespeed"): 0.07,
    # Video models
    ("veo-3.1", "google"): 0.50,
    ("kling-3.0", "wavespeed"): 0.30,
    ("sora-2", "wavespeed"): 0.30,
    ("sora-2-pro", "wavespeed"): 0.30,
}

# --- Default Models ---
DEFAULT_IMAGE_MODEL = "nano-banana-pro"
DEFAULT_VIDEO_MODEL = "veo-3.1"

# --- Directories ---
INPUTS_DIR = PROJECT_ROOT / "references" / "inputs"

# --- Video Models ---
VIDEO_MODELS = {
    "veo-3.1": "veo-3.1-generate-preview",
}

# --- Video Models (WaveSpeed AI) ---
# Same models available through WaveSpeed's infrastructure.
# WaveSpeed uses model ID in the URL path (not request body).
WAVESPEED_VIDEO_MODELS = {
    "kling-3.0": "kwaivgi/kling-v3.0-pro/image-to-video",
    "kling-3.0-std": "kwaivgi/kling-v3.0-std/image-to-video",
    "sora-2": "openai/sora-2/image-to-video",
    "sora-2-pro": "openai/sora-2/image-to-video-pro",
}


def get_cost(model, provider=None):
    """
    Get the cost per generation for a model+provider combination.

    Args:
        model: Model name (e.g., "nano-banana-pro", "veo-3.1")
        provider: Provider name (e.g., "google", "kie"). If None, uses default.

    Returns:
        float: Cost per unit
    """
    if provider is None:
        # Import here to avoid circular imports
        from .providers import IMAGE_PROVIDERS, VIDEO_PROVIDERS
        if model in IMAGE_PROVIDERS:
            provider = IMAGE_PROVIDERS[model]["default"]
        elif model in VIDEO_PROVIDERS:
            provider = VIDEO_PROVIDERS[model]["default"]
        else:
            return 0.0
    return COSTS.get((model, provider), 0.0)


def check_credentials():
    """Verify required API keys are set. Returns list of missing keys."""
    required = {
        "AIRTABLE_API_KEY": AIRTABLE_API_KEY,
        "AIRTABLE_BASE_ID": AIRTABLE_BASE_ID,
    }
    missing = [name for name, value in required.items() if not value]

    # At least one generation provider must be configured
    if not GOOGLE_AISTUDIO_API_KEY:
        missing.append("GOOGLE_AISTUDIO_API_KEY (required for image/video generation)")

    if missing:
        print("Missing API keys:")
        for key in missing:
            print(f"  - {key}")
        print(f"\nAdd them to: {ENV_PATH}")
    return missing


def check_wavespeed_credentials():
    """Verify WaveSpeed API key + Airtable keys are set. Returns list of missing keys."""
    required = {
        "WAVESPEED_API_KEY": WAVESPEED_API_KEY,
        "AIRTABLE_API_KEY": AIRTABLE_API_KEY,
        "AIRTABLE_BASE_ID": AIRTABLE_BASE_ID,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        print("Missing API keys:")
        for key in missing:
            print(f"  - {key}")
        print(f"\nAdd them to: {ENV_PATH}")
    return missing
