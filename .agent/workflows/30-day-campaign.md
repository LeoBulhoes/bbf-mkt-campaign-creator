---
description: Create a 30-day marketing campaign with daily scheduled posts — from brand discovery to autopilot
---

# 30-Day Marketing Campaign Workflow

This workflow creates a complete 30-day content calendar with unique AI-generated images and brand-voice captions, then schedules them one-per-day on autopilot via Blotato.

---

## Prerequisites

- Blotato account connected (Optional — skip if no `BLOTATO_API_KEY`)
- `BLOTATO_API_KEY` set in `.env` (Optional)
- Airtable configured (API key, base ID, Content table created)
- A `references/[brandname]_BRAND.md` file (created in Phase 1 if it doesn't exist)

---

## Phase 1: Brand Discovery → `brand.md`

**Goal:** Create a `references/[brandname]_BRAND.md` file that captures the brand's voice, values, audience, and visual identity. This file is the foundation for all content.

### Option A: Interview Method (Steven Bartlett Style)

If no brand.md exists yet, conduct a deep-dive interview. Ask the user these questions **one at a time**, building on their answers like a podcast host:

**Round 1 — Identity**
1. "What does your brand actually DO — in one sentence, like you're telling a stranger at a bar?"
2. "Who is the ONE person you're really talking to? Not a demographic — give me a real person. What keeps them up at night?"
3. "If your brand were a person at a dinner party, how would they talk? Formal? Casual? Provocative? Warm?"

**Round 2 — Values & Differentiation**
4. "What do you believe that most people in your industry would disagree with?"
5. "What's the FEELING you want someone to have after consuming your content?"
6. "Name 3 brands or creators whose style you admire — and tell me WHY for each one."

**Round 3 — Visual & Content Identity**
7. "Describe your ideal aesthetic in 3 words. If your brand were a movie set, what would it look like?"
8. "What content pillars do you keep coming back to? The 3-5 topics you could talk about forever?"
9. "What does your brand NEVER do? What's off-limits in tone, content, or style?"

**Round 4 — Goals & Platform**
10. "What platforms are you focusing on, and what does success look like in 30 days?"

After the interview, write `references/[brandname]_BRAND.md` using the template below.

### Option B: Content Analysis Method

If the user provides existing content (posts, videos, images, website):

1. **Analyze the content** — Use `mcp_blotato_blotato_create_source` to extract content from URLs:
   - YouTube videos → extract transcript, analyze speaking style
   - Articles/blog posts → extract voice, recurring themes
   - Social media posts → identify patterns, hashtags, engagement style

2. **Study visual patterns** — If images are provided, use `view_file` to analyze:
   - Color palette
   - Photography style (lifestyle, product, minimalist, etc.)
   - Typography preferences
   - Recurring visual elements

3. **Synthesize into brand.md** using the same template below.

### Brand.md Template

Write the file to `references/[brandname]_BRAND.md` with this structure:

```markdown
# [Brand Name] — Brand Voice & Style Guide

## Who We Are
- One-sentence mission
- Core product/service
- Stage of business (startup, growing, established)

## Target Audience
- **The Person:** [Name a specific archetype]
- **Their Pain:** What keeps them up at night
- **Their Desire:** What transformation they want
- **Where they hang out:** Platforms, communities

## Tone & Voice
| Attribute    | Description |
|------------- |-------------|
| Formality    | [e.g., Professional-casual] |
| Energy       | [e.g., High-energy, calm authority] |
| Humor        | [e.g., Witty one-liners, no humor, sarcastic] |
| Warmth       | [e.g., Direct but encouraging] |

### Signature Phrases
- [Any catchphrases, recurring language patterns]

### What We NEVER Do
- ❌ [Off-limits tones, topics, styles]

## Visual Identity
- **Color Palette:** [Primary, secondary, accent colors]
- **Aesthetic:** [3 words, e.g., "clean, bold, futuristic"]
- **Photography Style:** [e.g., lifestyle, studio, UGC-style]
- **Typography Feel:** [e.g., modern sans-serif, elegant serif]

## Content Pillars
1. [Pillar 1 — topic + why it matters]
2. [Pillar 2]
3. [Pillar 3]
4. [Pillar 4 — optional]
5. [Pillar 5 — optional]

## Platform Strategy
- **Primary:** [Platform] — [posting frequency, content type]
- **Secondary:** [Platform] — [adapted approach]

## Inspirations
- [Brand/Creator 1] — what we take from them
- [Brand/Creator 2]
- [Brand/Creator 3]
```

---

## Phase 2: Create the 30-Day Content Calendar in Airtable

**Goal:** Create a 30-day content calendar with a mix of **1 to 4 distinct products per day**. Each product for a given day should have its own record in Airtable (individual ad) with a unique Image Prompt, Caption, and Scheduled Date. The user reviews everything in Airtable BEFORE any images are generated.

### Step 2.1: Read the Brand File

```
Read references/[brandname]_BRAND.md to understand the brand's voice, audience, pillars, and visual style.
```

### Step 2.2: Upload Reference Images

Upload the product reference image(s) to GCP so they can be attached to every Airtable record:

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

### Step 2.3: Plan the 30 Posts

Design 30 unique posts that **utilize the entire product catalog** (rotate through all available reference images in the `products/` folder) and:

1. **Rotate through specific Styles** — follow this distribution exactly and dont use the examples to filter products or categories:

| Style | Distribution | Prompt Formula Example |
| :--- | :--- | :--- |
| **Candid Play (UGC)** | ~8 Posts | `A child laughing on a bright playground wearing this t-shirt, authentic social media vibe.` |
| **Sports Hero** | ~7 Posts | `A teenager in a power stance on a grass soccer field wearing this hoodie. Focused energy.` |
| **Quality Detail** | ~5 Posts | `Extreme close-up detail shot of this t-shirt focusing on fabric and stitching, shallow depth of field.` |
| **Nature/Outdoor** | ~5 Posts | `A person walking through a sun-drenched forest trail wearing this hoodie. Golden hour.` |
| **Cozy Spaces** | ~3 Posts | `A student relaxing in a cozy library nook wearing this t-shirt. Calm confidence.` |
| **School Flat Lay** | ~2 Posts | `Overhead shot of this cap and this sticker on a wooden school desk with notebooks.` |

2. **Follow the Weekly Rhythm strictly** (mapping these styles to days):
   - **Monday:** Motivational / Brand statement (Style: Nature/Outdoor)
   - **Tuesday:** Product detail close-up (Style: Quality Detail)
   - **Wednesday:** UGC selfie-style (Style: Candid Play)
   - **Thursday:** Studio hero shot (Style: Sports Hero or Quality Detail)
   - **Friday:** Urban lifestyle (Style: Nature/Outdoor)
   - **Saturday:** World-building / CGI (Style: Nature/Outdoor)
   - **Sunday:** Community engagement (Style: Cozy Spaces or Candid Play)

3. **Write brand-voice captions** following the brand file's caption guidelines:
   - Include relevant emojis (from brand guide)
   - Include 2-3 hashtags (from brand guide)
   - Include a CTA (call-to-action)
   - Match the tone exactly

### Step 2.4: Create 30 Airtable Records

Use `create_records_batch` to create all records (averaging 1-4 per day). Each record gets:

```python
{
    "Index": start_index + i,
    "Ad Name": "[image types] - Day 1 - UGC Selfie",
    "Product": "[image types] Product",
    "Reference Images": [{"url": ref_url}],
    "Image Prompt": "9:16. ...",
    "Image Model": "Nano Banana Pro",
    "Image Status": "Pending",
    "Generated Image 1": [],
    "Masked Image 1": [],
    "Caption": "...",
    "Scheduled Date": "2026-02-25T10:00:00+11:00",
}
```

**IMPORTANT:** Increment `Scheduled Date` by 1 day for each record (Day 1 = start date, Day 30 = start date + 29 days).

### Step 2.5: Review Checkpoint

**STOP and tell the user to review everything in Airtable.**

Show:
- A summary of the image type distribution (e.g., "UGC: 8, Studio: 7, Detail: 5...")
- 3-5 sample captions with their prompts
- The date range (start → end)

Ask: "I've created all 30 dates in Airtable with prompts, captions, and scheduled dates. Head over to Airtable to review them — you can edit any captions or prompts before I generate the images. Let me know when you're happy with everything!"

**Do NOT proceed to image generation until the user approves.**

---

## Phase 3: Generate All pending Images

**Goal:** Generate unique images for each of the pending Airtable records using Nano Banana Pro via Google AI Studio.

### Step 3.1: Cost Estimate

Before generating, show the cost:
- **[count of images] Pending images × $0.13 each = ~$3.90 total** (Nano Banana Pro via Google)
- **2 variations per record = 1 images total = ~$7.80** (if doing 2 variations)
- Estimated time: ~60-90 minutes for all [count of images] records

Ask: "This will generate [count of images] images using Nano Banana Pro (Google AI Studio) at ~$0.13 each. Total cost: ~$3.90 for 1 variation per record, or ~$7.80 for 2 variations. Which would you prefer?"

### Step 3.2: Generate Images

Use the existing image generation pipeline:

```python
import sys; sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv('references/.env')
from tools.airtable import get_pending_images
from tools.image_gen import generate_batch

records = get_pending_images()
results = generate_batch(
    records,
    model="nano-banana-pro",
    provider="google",
    num_variations=1,  # or 2 if user chose 2
)
```

This will:
1. Read all records with `Image Status = "Pending"` from Airtable
2. Generate an image for each record using its `Image Prompt`
3. Upload the generated image to GCP hosting
4. Attach the image URL back to the Airtable record (`Generated Image 1`)
5. Update `Image Status` to `"Generated"`

### Step 3.3: Review Checkpoint

After all images are generated, tell the user:

"All [count of images] images are generated and visible in Airtable! Check the 'Masked Image 1' and 'Generated Image 1' column. Mark any you love as 'Approved' and anything you want redone as 'Rejected'. I can regenerate rejected ones with tweaked prompts."

**Do NOT proceed to video generation or scheduling until the user confirms.**
**Ask user if he wants to generate video prompt.**

---

## Phase 3.5: Generate Videos (Optional)

**Goal:** Convert select approved images into short-form videos using Veo 3.1 (Google AI Studio). Not all  posts need video — typically 8-12 is ideal for a mix of static and video content.

### Step 3.5.1: Select Records for Video

Ask the user which posts should get video versions. Recommend:
- **UGC / Selfie posts** — great for Reels/TikTok (subtle head turns, selfie motions)
- **Studio Hero Shots** — dramatic reveals (wind, slow push-in)
- **Urban Lifestyle** — walking/motion scenes

Set the `Video Prompt` field in Airtable for each selected record. Video prompts should:
- Start with "Starting from the image..."
- Describe motion (what moves, how)
- Specify camera movement (push-in, orbit, tracking)
- Reference `references/docs/prompt-best-practices.md` for guidance

### Step 3.5.2: Cost Estimate

Before generating, show the cost:
- **Veo 3.1: ~$0.50 per video**
- Example: 10 videos = ~$5.00
- Estimated time: ~3-5 minutes per video

Ask: "This will generate [N] videos using Veo 3.1 at ~$0.50 each. Total cost: ~$[total]. Proceed?"
**Do NOT proceed to video generation until the user approves, confirms or requests.**

### Step 3.5.3: Generate Videos

```python
import sys; sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv('references/.env')
from tools.airtable import get_pending_videos
from tools.video_gen import generate_batch

records = get_pending_videos()
results = generate_batch(
    records,
    model="veo-3.1",
    duration="8",
    aspect_ratio="9:16",
    num_variations=1,
)
```

This will:
1. Read all records with `Video Status = "Pending"` from Airtable
2. Use `Generated Image 1` as the source frame for each video
3. Generate a video based on the `Video Prompt`
4. Upload the video to GCP hosting
5. Attach the video URL to `Generated Video 1`
6. Update `Video Status` to `"Generated"`

### Step 3.5.4: Review Checkpoint

"All videos are generated and visible in Airtable! Check the 'Generated Video 1' column. Mark any you love as 'Approved' and anything you want redone as 'Rejected'. I can regenerate rejected ones with tweaked prompts."

**Do NOT proceed to scheduling until the user confirms.**

---


## Key Rules

1. **Brand.md is mandatory** — never generate content without understanding the brand first
2. **Airtable is the review hub** — all prompts, captions, images, and videos live in Airtable so the user can review
3. **User approves at every checkpoint** — Airtable review, image review, video review, schedule confirmation
4. **Cost transparency** — show estimated costs before any generation (images AND videos)
5. **Default models** — Nano Banana Pro for images, Veo 3.1 for videos
6. **Track everything** — schedule log saved to `references/outputs/schedule_log.md`
7. **Platform-specific adjustments:**
   - **Instagram**: images as regular posts, videos as Reels (`mediaType: "reel"`), 30 hashtags max
   - **TikTok**: Use 9:16, set `privacyLevel`, `disabledComments: false`, `isAiGenerated: true`
   - **YouTube**: Use 16:9, requires `title`, `privacyStatus`, `shouldNotifySubscribers`
8. **Use the Blotato posting skill** — when using local files, follow `.agent/skills/blotato_best_practices/SKILL.md`
9. **Caption quality** — every caption must match the brand voice from brand.md, include emojis, hashtags, and a CTA
10. **Content variety** — rotate through UGC, studio, detail, lifestyle, CGI, and flat lay styles
11. **Video from image** — always generate and approve images BEFORE generating videos
12. **Scheduling timezone** — use the user's timezone from the metadata timestamp offset
13. **Airtable batch limits** — records are created in batches of 10 (handled automatically by `create_records_batch`)
