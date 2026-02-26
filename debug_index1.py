import sys, os
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv('references/.env')
from tools.providers.google import submit_image

# Use the actual product photo, not the logo
ref_path = "references/brands/bluebullfly/products/kids_cotton_tee_front.jpg"

prompt = "9:16. Create a picture of a child playing on a playground wearing this t-shirt."

print(f"Ref: {ref_path}")
print(f"Prompt: {prompt}\n")
print("Submitting to Google AI Studio (Nano Banana Pro)...")

try:
    result = submit_image(prompt, reference_paths=[ref_path], aspect_ratio="9:16", resolution="1K", model="nano-banana-pro")
    print(f"\n--- SUCCESS ---\nURL: {result.get('result_url')}")
except Exception as e:
    print(f"\n--- FAILED ---\n{e}")
