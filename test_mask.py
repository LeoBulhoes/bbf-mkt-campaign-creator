import requests
from io import BytesIO
from PIL import Image
import os
import sys

# Get mask
mask_path = "references/brands/bluebullfly/logo/Ad Mask.png"
if not os.path.exists(mask_path):
    print("Mask not found!")
    sys.exit(1)

# Generate a dummy image (like the solid blue background)
img = Image.new('RGB', (1080, 1920), color=(0, 85, 255))
img = img.convert("RGBA")

# Load mask
mask = Image.open(mask_path).convert("RGBA")

mask_w, mask_h = mask.size
img_w, img_h = img.size

print(f"Original image size: {img_w}x{img_h}")
print(f"Mask size: {mask_w}x{mask_h}")

if mask_w > img_w or mask_h > img_h:
    print("Resizing mask to fit")
    mask.thumbnail((img_w, img_h), Image.Resampling.LANCZOS)

img.alpha_composite(mask, (0, 0))

out_path = "test_masked_output.jpg"
img.convert("RGB").save(out_path, format="JPEG")
print(f"Saved masked image to {out_path}")
