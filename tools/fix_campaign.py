
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

sys.path.insert(0, '.')
load_dotenv('references/.env')
from tools.gcp_upload import upload_reference
from tools.airtable import create_records_batch, get_next_index, create_ugc_table

# Products in references/brands/bluebullfly/products (as listed in Step 19)
# Note: User said "respect the products in references/brands/bluebullfly/products and added the hoodie to the mix"
# This implies I should list that directory and use what's there.
PRODUCT_DIR = 'references/brands/bluebullfly/products'

def get_available_products():
    products = []
    for f in os.listdir(PRODUCT_DIR):
        if f.endswith('.jpg') or f.endswith('.png'):
            # Parse product name and variation from filename
            # e.g., kids_cotton_tee_back.jpg -> Name: Kids Cotton Tee, Variation: Back
            base = os.path.splitext(f)[0]
            parts = base.split('_')
            # Heuristic for name vs variation
            if len(parts) >= 2:
                variation = parts[-1]
                name = ' '.join(parts[:-1]).title()
            else:
                name = base.title()
                variation = "Default"
            
            products.append({
                'path': os.path.join(PRODUCT_DIR, f),
                'name': name,
                'variation': variation,
                'filename': base
            })
    return products

PILLARS = [
    "Adventure Ready",
    "Quality Matters",
    "Style That Stands Out",
    "Back to School"
]

IMAGE_TYPES = [
    ("UGC Selfie", "9:16. A child taking a selfie in a [PRODUCT] in their bedroom. Natural lighting, phone-in-hand feel."),
    ("Studio Hero Shot", "9:16. A child model wearing a [PRODUCT] against a clean concrete wall. Dramatic studio lighting."),
    ("Close-up Detail", "9:16. Extreme macro shot of the high-quality fabric and stitching on a [PRODUCT]."),
    ("Urban Lifestyle", "9:16. A child playing in a vibrant urban park wearing a [PRODUCT]. Candid motion, warm lighting."),
    ("CGI/World-Building", "9:16. A digital 3D render of a [PRODUCT] surrounded by glowing blue butterflies in a clean white space."),
    ("Flat Lay", "9:16. A [PRODUCT] laid out on a clean white surface with school supplies.")
]

def run_campaign_day_1():
    # 1. Initialize Table
    create_ugc_table()
    
    # 2. Get Products
    products = get_available_products()
    if not products:
        print("No products found in references/brands/bluebullfly/products")
        return

    # 3. Upload Reference Images with custom naming
    # Store reference images in bucket using product name and variation as filename
    for p in products:
        custom_name = f"references/{p['filename']}"
        p['url'] = upload_reference(p['path'], custom_name=custom_name)

    # 4. Plan 30 records but user said "run @/30-day-campaign for day 1"
    # This usually means starting the 30-day cycle but we focus on creation.
    # I'll generate the full 30 days as requested by the workflow, but clearly they had issues with my previous script.
    
    records = []
    start_date = datetime(2026, 2, 27, 10, 0, 0)
    current_index = get_next_index()
    
    for day in range(30):
        # Rotate through products
        p = products[day % len(products)]
        product_name = f"{p['name']} ({p['variation']})"
        ref_url = p['url']

        pillar = PILLARS[day % len(PILLARS)]
        type_name, prompt_tmpl = IMAGE_TYPES[day % len(IMAGE_TYPES)]
        
        scheduled_date = (start_date + timedelta(days=day)).isoformat() + "-06:00"
        
        # Caption generation
        if pillar == "Adventure Ready":
            caption = f"Ready for action! 🦋 Our {p['name']} is built for playground battles. 💪\n\nPlay All Day. Built to Last.\n\nShop at bluebullfly.com ☀️\n\n#bluebullfly #playallday"
        elif pillar == "Quality Matters":
            caption = f"Quality you can feel. 🎒 Performance-grade fabric that survives every adventure. 🦋\n\nCozy Warmth. Built for School.\n\nLink in bio! ✨\n\n#quality #kidsclothes #bluebullfly"
        elif pillar == "Style That Stands Out":
            caption = f"Stand out on the playground! 🌈 Trendy {p['name']} with a pop of fun. 🦋\n\nEveryday Adventures start here. ☀️\n\nbluebullfly.com\n\n#kidsstyle #butterfly #funfashion"
        else: # Back to School
            caption = f"School ready, play ready. 🎒 The {p['name']} is a classroom favorite! 🦋\n\nBuilt to Last.\n\nShop the drop! 💪\n\n#backtoschool #bluebullfly #essentials"

        prompt = prompt_tmpl.replace("[PRODUCT]", f"this {p['name']}")
        
        records.append({
            "Index": current_index + day,
            "Ad Name": f"BBF - Day {day+1} - {type_name}_{p['filename']}_ad",
            "Product": p['name'],
            "Reference Images": [{"url": ref_url}],
            "Image Prompt": prompt,
            "Image Model": "Nano Banana Pro",
            "Image Status": "Pending",
            "Caption": caption,
            "Scheduled Date": scheduled_date,
        })
    
    print(f"Creating {len(records)} records...")
    create_records_batch(records)
    print("Done!")

if __name__ == "__main__":
    run_campaign_day_1()
