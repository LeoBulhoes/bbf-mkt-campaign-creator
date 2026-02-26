---
description: Create a 1-day marketing campaign with daily scheduled posts — from brand discovery to autopilot
---

# 1-Day Marketing Campaign Workflow

This workflow creates a single high-impact marketing post with an AI-generated image and brand-voice caption, then schedules it via Blotato.

---

## Prerequisites

- Blotato account connected (Optional — skip if no `BLOTATO_API_KEY`)
- `BLOTATO_API_KEY` set in `.env` (Optional)
- Airtable configured (API key, base ID, Content table created)
- A `references/[brandname]_BRAND.md` file (created in Phase 1 if it doesn't exist)

---

## Phase 1: Brand Discovery → `brand.md`

**Goal:** Create a `references/[brandname]_BRAND.md` file that captures the brand's voice, values, audience, and visual identity.

*(Same as 30-Day Workflow)*

---

## Phase 2: Create the 1-Day Content Record in Airtable

**Goal:** Create 1 record in Airtable with a unique Image Prompt, Caption, and Scheduled Date.

### Step 2.1: Read the Brand File

```
Read references/[brandname]_BRAND.md to understand the brand's voice, audience, pillars, and visual style.
```

### Step 2.2: Upload Reference Images

Upload the product reference image(s) to GCP:

```python
python -c "
import sys; sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv('references/.env')
from tools.gcp_upload import upload_references
ref_urls = upload_references(['references/[brandname]/products/product.jpg'])
f = open('references/outputs/ref_urls.txt', 'w'); f.write('\n'.join(ref_urls)); f.close()
print('Reference URLs saved.')
"
```

### Step 2.3: Plan the Post

Design 1 post that:
1. Matches a selected **content pillar**.
2. Uses a specific **image type** (UGC, Studio, Detail, Urban, CGI, or Flat Lay).
3. Follows the **brand-voice guidelines** for the caption.

### Step 2.4: Create Airtable Record

Use `create_record` to create the entry.

```python
{
    "Index": start_index,
    "Ad Name": "Hero - Day 1 - UGC Selfie",
    "Product": "Hero Product",
    "Reference Images": [{"url": ref_url}],
    "Image Prompt": "9:16. ...",
    "Image Model": "Nano Banana Pro",
    "Image Status": "Pending",
    "Caption": "...",
    "Scheduled Date": "2026-02-27T10:00:00-06:00",
}
```

---

## Phase 3: Generate Image

**Goal:** Generate the image using Nano Banana Pro.

### Step 3.1: Generate Image

```python
import sys; sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv('references/.env')
from tools.airtable import get_pending_images
from tools.image_gen import generate_batch

records = get_pending_images()
results = generate_batch(
    records,
    model="nano-banana-pro",
)
```

---

## Phase 4: Schedule via Blotato (OR Manual Mode)

**Goal:** Schedule the approved post.

*(Same as 30-Day Workflow but for 1 record)*
