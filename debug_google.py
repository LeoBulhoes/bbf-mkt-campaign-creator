import sys, os, json
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv('references/.env')
from tools.providers.google import submit_image
from tools.utils import download_temp_file

# Index 1 prompt
prompt = '9:16. A 6-year-old child wearing the Bluebullfly Kids Cotton T-Shirt, playing actively on a colorful outdoor playground. High energy, natural daylight, candid lifestyle photography. The T-shirt should be clearly visible. Using input image 1 for product identity.'

# Download references for Index 1 (we have urls[0] and urls[5])
# Wait, let's just use the local file from references directly
ref_img = 'references/products/bluebullfly-kids-cotton-crew-neck-t-shirt-royal-10655-66299b66bb7dc.jpg'

print('Calling submit_image...')
try:
    res = submit_image(prompt, reference_paths=[ref_img], aspect_ratio="9:16", resolution="1K", model="nano-banana-pro")
    print("SUCCESS Result:", res)
except Exception as e:
    print("ERROR:", e)

