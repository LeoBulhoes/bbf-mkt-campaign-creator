---
description: Clone a winning ad — analyze it, break into scenes, regenerate with your product and brand
---

# Clone Winning Ad Workflow

Reverse-engineer a successful ad and recreate it with your own product. Give the agent a reference ad (video URL, local file, or image) and it produces a full set of branded content ready for scheduling.

---

## Prerequisites

- A reference ad to clone (YouTube/TikTok/Instagram URL, local video file, or screenshot)
- Product reference image(s) in `references/inputs/`
- A `references/[brandname]_BRAND.md` file (use `/30-day-campaign` Phase 1 to create one)
- Airtable configured with the Content table

---

## Phase 1: Analyze the Reference Ad

**Goal:** Break the winning ad into individual scenes with detailed descriptions.

### Step 1.1: Ingest the Reference Ad

Depending on what the user provides:

**If it's a URL (YouTube, TikTok, Instagram):**
1. Use `mcp_blotato_blotato_create_source` to extract content metadata
2. Ask the user to describe the key scenes if transcript/visual analysis isn't enough

**If it's a local video file:**
1. Note: video files cannot be directly analyzed visually
2. Ask the user to describe the scenes, OR
3. Extract key frames using ffmpeg (if available):
   ```bash
   ffmpeg -i references/inputs/reference_ad.mp4 -vf "fps=1" references/outputs/frame_%03d.jpg
   ```
4. Analyze extracted frames with `view_file`

**If it's an image or screenshot:**
1. Use `view_file` to analyze it directly
2. Identify composition, lighting, product placement, and mood

### Step 1.2: Scene Breakdown

Create a scene-by-scene storyboard. For each scene, document:

| Scene | Duration | Visual Description | Motion/Action | Mood/Energy |
|-------|----------|-------------------|---------------|-------------|
| 1 | 1-2s | Close-up detail shot, dark background | Slow reveal, camera push-in | Mysterious, anticipation |
| 2 | 2-3s | Model wearing product, urban rooftop | Turns toward camera | Confident, cool |
| 3 | 2-3s | Product detail: zipper, stitching | Slow orbit around product | Premium, craftsmanship |
| 4 | 1-2s | Full body hero shot, dramatic lighting | Wind blows jacket fabric | Powerful, aspirational |
| 5 | 1s | Brand logo / CTA text overlay | Static hold | Clean, direct |

Save this breakdown to `references/outputs/scene_breakdown.md`.

### Step 1.3: Adaptation Plan

For each scene, plan how to recreate it with the user's product:
- Replace the original product with the user's product (reference images)
- Adapt the setting to match the brand's visual identity (from `*_BRAND.md`)
- Keep the hook structure and pacing from the original
- Match the emotional arc (mysterious → confident → premium → powerful → CTA)

---

## Phase 2: Generate Image Prompts

**Goal:** Write image prompts for each scene that will produce the starting frames.

### Step 2.1: Read Brand File

```
Read references/[brandname]_BRAND.md for voice, audience, pillars, and visual style.
```

### Step 2.2: Upload Reference Images

```python
python -c "
import sys; sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv('references/.env')
from tools.kie_upload import upload_references
ref_urls = upload_references(['references/inputs/product.jpg'])
f = open('references/outputs/ref_urls.txt', 'w'); f.write('\n'.join(ref_urls)); f.close()
print('Reference URLs saved.')
"
```

### Step 2.3: Write Prompts per Scene

For each scene in the storyboard, write:
- **Image Prompt** — recreate the scene composition with the user's product
- **Video Prompt** — describe the motion/transition for that scene
- **Caption** — brand-voice caption for the final post

Follow `references/docs/prompt-best-practices.md` for prompt structure.

**Image prompt format:**
```
9:16. [Scene description with user's product]. [Lighting]. [Camera angle].
Reference the product naturally: "wearing this jacket", "holding this product", etc.
```

**Video prompt format:**
```
Starting from the image, [describe what moves/changes].
[Camera movement]. [Atmosphere details].
```

### Step 2.4: Create Airtable Records

Use `create_records_batch` to create one record per scene:

```python
{
    "Index": start_index + i,
    "Ad Name": "Clone - Scene 1 - Hook Detail",
    "Product": "User's Product Name",
    "Reference Images": [{"url": ref_url}],
    "Image Prompt": "9:16. Extreme close-up of product zipper...",
    "Image Model": "Nano Banana Pro",
    "Image Status": "Pending",
    "Video Prompt": "Starting from the image, slow camera push-in...",
    "Video Model": "Veo 3.1",
    "Video Status": "Pending",
    "Caption": "Brand-voice caption with emojis and CTA",
    "Scheduled Date": "2026-02-25T16:00:00-06:00",
}
```

### Step 2.5: Review Checkpoint

**STOP and tell the user to review in Airtable.**

Show:
- Scene-by-scene summary with image type and original reference
- 2-3 sample prompts with their video prompts
- Total record count

"I've recreated [N] scenes from the reference ad in Airtable with image prompts, video prompts, and captions. Head over to Airtable to review — you can edit any prompts before I generate. Let me know when you're happy!"

**Do NOT proceed until approved.**

---

## Phase 3: Generate Images

**Goal:** Generate the starting frame images for each scene.

### Step 3.1: Cost Estimate

Show: `N scenes × $0.13 (Nano Banana Pro) = $X.XX`

### Step 3.2: Generate

```python
import sys; sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv('references/.env')
from tools.airtable import get_pending_images
from tools.image_gen import generate_batch

records = get_pending_images()
results = generate_batch(
    records,
    reference_paths=["references/inputs/product.jpg"],
    model="nano-banana-pro",
    provider="google",
    num_variations=1,
)
```

### Step 3.3: Review Checkpoint

"All scene images are generated! Check Airtable — mark as Approved or Rejected."

---

## Phase 4: Generate Videos

**Goal:** Animate each approved scene image into a short video clip.

### Step 4.1: Cost Estimate

Show: `N scenes × $0.50 (Veo 3.1) = $X.XX`

### Step 4.2: Generate

```python
import sys; sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv('references/.env')
from tools.airtable import get_pending_videos
from tools.video_gen import generate_batch

records = get_pending_videos()
results = generate_batch(
    records,
    model="veo-3.1",
    duration="6",
    aspect_ratio="9:16",
    num_variations=1,
)
```

### Step 4.3: Review Checkpoint

"All scene videos are generated! Check the 'Generated Video 1' column in Airtable. Mark as Approved or Rejected."

---

## Phase 5: Schedule via Blotato (OR Manual Mode)

**Goal:** Schedule the approved content as posts, or save for manual upload if Blotato is unavailable.

### Manual Mode (If no Blotato API Key)
If `BLOTATO_API_KEY` is missing:
1. Provide the user with the Final Image/Video download links from Kie.ai.
2. Provide the matching captions.
3. Instruct the user to post manually to their preferred platforms.

### Step 5.1: Confirm Settings

Ask the user:
1. Which platform(s) to post to?
2. Post timing (all at once, or staggered over days)?
3. For video posts: Instagram Reels, TikTok, YouTube Shorts?

### Step 5.2: Schedule Posts

For each approved record:
1. Get the generated video URL (or image URL if no video)
2. Schedule via `mcp_blotato_blotato_create_post`
3. For video posts on Instagram, set `mediaType: "reel"`
4. For TikTok, include all required fields (`privacyLevel`, `isAiGenerated: true`, etc.)

### Step 5.3: Final Summary

Present:
- ✅ Total posts scheduled
- 📅 Date range
- 📱 Platform(s)
- 🖼️ Images: X, Videos: X
- 💰 Total generation cost

---

## Key Rules

1. **Original ad is inspiration, not copy** — adapt the structure and pacing, but create original content with the user's product
2. **User approves at every checkpoint** — scene breakdown, prompts, images, videos, schedule
3. **Cost transparency** — show costs before each generation phase
4. **Brand consistency** — all content must match the `*_BRAND.md` file
5. **Reference images are critical** — use them in every image prompt for product consistency
6. **Video from image, always** — generate and approve images BEFORE generating videos
