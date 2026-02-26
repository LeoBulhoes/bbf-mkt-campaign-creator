---
description: Create a 7-day kickoff campaign with daily posts — from brand verification to manual posting
---

# 7-Day Kickoff Campaign Workflow

This workflow creates a focused 7-day content calendar designed to "kickstart" a new brand profile. It produces a professional mix of high-detail images and high-motion videos, ready for manual upload to Instagram, TikTok, and YouTube.

---

## Prerequisites

- Airtable configured (API key, base ID, Content table created)
- A `references/[brandname]_BRAND.md` file verified by the user
- Product reference images in `references/inputs/`
- `GCP_BUCKET_NAME` and `GOOGLE_API_KEY` set in `.env`

---

## Phase 1: Brand Verification

**Goal:** Ensure the brand identity is correctly captured. If `bluebullfly_BRAND.md` already exists, confirm with the user that the "Adventure Ready" and "Quality Matters" pillars are still the priority for the 7-day launch.

---

## Phase 2: Create the 7-Day Content Calendar in Airtable

**Goal:** Create 7 records in Airtable with unique prompts and captions.

### Step 2.1: Plan the 7 Posts (The Sprint Strategy)
Design a sequence that builds trust:
1. **Day 1**: Hero Product Hook (Video) - High energy playground shot.
2. **Day 2**: Material Detail (Image) - Close-up on DryBlend performance fabric.
3. **Day 3**: Lifestyle / School (Image) - Hoodie hero shot in a natural setting.
4. **Day 4**: Accessories Mix (Image) - Flat-lay of cap and mugs.
5. **Day 5**: Feature Reveal (Video) - Zoom-in on the butterfly print quality.
6. **Day 6**: Lifestyle Variety (Image) - Multiple tees in different brand colors.
7. **Day 7**: Grand Finale (Video) - Brand vision / Logo reveal with kids playing.

### Step 2.2: Create Records
Use `create_records_batch` to populate Airtable with prompts and ISO dates for the next 7 days.

---

## Phase 3: Generation (Images & Videos)

**Goal:** Produce 7 high-quality assets.

1. **Step 3.1: Generate Images** (Nano Banana Pro)
   - Cost: 7 images × $0.13 = **$0.91**
2. **Step 3.2: Generate Videos** (Veo 3.1)
   - Convert approved images from Days 1, 5, and 7.
   - Cost: 3 videos × $0.50 = **$1.50**

---

## Phase 4: Manual Posting Mode

Since `BLOTATO_API_KEY` is not required for this kickoff:

1. **Gather Links**: Retrieve the GCP URLs for the 7 generated files.
2. **Export Log**: Create a table in the chat or a `.md` file with:
   - **Date/Time**
   - **Download Link** (the GCP URL)
   - **Caption to Copy**
3. **Post Manually**: The user downloads and uploads to their social accounts.

---

## Key Rules
1. **Always use Google Providers**: Nano Banana Pro (Image) and Veo 3.1 (Video).
2. **Cost Confimation**: Always show the **~$2.41** estimate before starting.
3. **Airtable First**: Never generate until the prompts are in Airtable for user review.
