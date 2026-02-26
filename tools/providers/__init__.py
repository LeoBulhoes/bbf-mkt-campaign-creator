"""
Provider registry and routing for image and video generation.

Multi-provider architecture — routes to Google AI Studio (default),
Kie AI, or WaveSpeed based on model + provider selection.

Usage:
    from tools.providers import get_image_provider, get_video_provider, is_sync

    provider, name = get_image_provider("nano-banana-pro")  # Google (default)
    provider, name = get_video_provider("veo-3.1")           # Google (default)
"""

from . import google

# --- Image model registry ---
IMAGE_PROVIDERS = {
    "nano-banana": {
        "default": "google",
        "providers": {"google": google},
    },
    "nano-banana-pro": {
        "default": "google",
        "providers": {"google": google},
    },
}

# --- Video model registry ---
VIDEO_PROVIDERS = {
    "veo-3.1": {
        "default": "google",
        "providers": {"google": google},
    },
}


def get_image_provider(model="nano-banana-pro", provider_override=None):
    """
    Get the provider module for an image model.

    Args:
        model: Image model name (e.g., "nano-banana-pro")
        provider_override: Force a specific provider (e.g., "google")

    Returns:
        tuple: (provider_module, provider_name)
    """
    model_config = IMAGE_PROVIDERS.get(model)
    if not model_config:
        raise ValueError(f"Unknown image model: '{model}'. Available: {list(IMAGE_PROVIDERS.keys())}")

    provider_name = provider_override or model_config["default"]
    provider = model_config["providers"].get(provider_name)
    if not provider:
        available = list(model_config["providers"].keys())
        raise ValueError(f"Provider '{provider_name}' not available for '{model}'. Available: {available}")

    return provider, provider_name


def get_video_provider(model="veo-3.1", provider_override=None):
    """
    Get the provider module for a video model.

    Args:
        model: Video model name (e.g., "veo-3.1")
        provider_override: Force a specific provider (e.g., "google")

    Returns:
        tuple: (provider_module, provider_name)
    """
    model_config = VIDEO_PROVIDERS.get(model)
    if not model_config:
        raise ValueError(f"Unknown video model: '{model}'. Available: {list(VIDEO_PROVIDERS.keys())}")

    provider_name = provider_override or model_config["default"]
    provider = model_config["providers"].get(provider_name)
    if not provider:
        available = list(model_config["providers"].keys())
        raise ValueError(f"Provider '{provider_name}' not available for '{model}'. Available: {available}")

    return provider, provider_name


def is_sync(provider_module, generation_type):
    """
    Check if a provider's generation is synchronous (no polling needed).

    Args:
        provider_module: The provider module (e.g., google)
        generation_type: "image" or "video"

    Returns:
        bool: True if synchronous (result returned immediately)
    """
    return getattr(provider_module, f"{generation_type}_IS_SYNC", False)
