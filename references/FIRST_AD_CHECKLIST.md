# 🦋 Bluebullfly — First Ad Checklist

> Goal: Get your first ad published on social media using the Marketing Bot.  
> Estimated time: ~45 minutes (excluding review/approval waits)

---

## Phase 0: Prerequisites (YOU do this)

- [ ] **1. Set up API keys** — Create or verify you have:
  - [ ] `GOOGLE_API_KEY` — from [Google AI Studio](https://aistudio.google.com/apikey)
  - [ ] `GCP_BUCKET_NAME` — Your Google Cloud Storage bucket name
  - [ ] `AIRTABLE_API_KEY` + `AIRTABLE_BASE_ID` — from [Airtable](https://airtable.com/create/tokens)
  - [ ] `BLOTATO_API_KEY` — from [Blotato](https://blotato.com) (for scheduling)

- [ ] **2. Add keys to `.env`** — Copy `references/.env.example` → `references/.env` and fill in values

- [ ] **3. Connect social accounts in Blotato** — Link your Instagram, TikTok, or Facebook accounts

- [ ] **4. Create an Airtable Base** — A blank base is fine; the agent will create the `Content` table

---

## Phase 1: Let the Agent Create Your First Ad (ASK the agent)

### Option A: Quick Single Ad (fastest path)

Tell the agent:
```
Using the bluebullfly_BRAND.md profile, create a single ad for our Kids Cotton 
Crew Neck Performance T-Shirt. Use the existing Ad 1 image from 
~/Leo/Bulhoes.org/Bluebullfly (local)/Pictures/Ad 1.png as the reference style. 
Create an Instagram Reel-ready post with caption. Schedule it for tomorrow at 10am CST.
```

### Option B: Clone an Existing Ad

Tell the agent:
```
/clone-ad

Reference: ~/Leo/Bulhoes.org/Bluebullfly (local)/Pictures/Ad 1.png
Product: Kids Cotton Crew Neck Performance T-Shirt
Brand: bluebullfly_BRAND.md
```

### Option C: Full 30-Day Campaign (comprehensive, but more time)

Tell the agent:
```
/30-day-campaign

Brand file: references/bluebullfly_BRAND.md
```

---

## Phase 2: Review & Approve (YOU do this)

- [ ] **5. Review the generated content** — The agent will show you:
  - Image/video preview
  - Caption text
  - Scheduled date/time
  - Cost estimate for AI generation

- [ ] **6. Approve generation costs** — Agent will show `$X.XX` estimate before generating

- [ ] **7. Review the final output** — Approve the image/video before scheduling

---

## Phase 3: Publish (Agent handles this)

- [ ] **8. Agent schedules via Blotato** — Post goes to your connected social accounts
- [ ] **9. Verify the post** — Check your social media account to confirm

---

## Recommended First Ad Strategy

### Best Product for First Ad
**Kids Cotton Crew Neck Performance T-Shirt** ($38.94)
- Unique all-over butterfly print (can't find elsewhere)
- Most visually distinctive product
- Shows the brand pattern clearly

### Best Ad Format
**Instagram Reel (9:16 video)** or **Instagram Feed Post (1:1 image)**

### Best Hook / Caption Style
```
🦋 Play All Day. Built to Last.

Soft cotton blend meets fun butterfly prints — the tee your kid 
will actually WANT to wear. 

✨ 96% Cotton, 4% Elastane
✨ All-over unique print
✨ Machine washable & pilling-resistant

🛒 Shop now → bluebullfly.com

#KidsFashion #KidsApparel #BlueBullFly #PlayAllDay #KidsStyle
```

### Best Time to Post
- **Weekdays**: 9–11 AM CST (parents browsing during morning routine)
- **Weekends**: 8–10 AM CST (family planning time)

---

## What You Already Have (no generation needed!)

You can post these **immediately** using the existing assets:

| Asset | Path | Best Platform |
|-------|------|--------------|
| Ad 1 (Playground slide) | `Pictures/Ad 1.png` | Instagram Feed |
| Ad 2 (Flat lay t-shirt) | `Pictures/Ad 2.png` | Instagram Feed |
| Ad 3 (Hoodie lifestyle) | `Pictures/Ad 3.png` | Instagram Feed |
| Promo Video 1 (16:9) | `Videos/Bluebullfly Video 1 16_9 complete.mp4` | YouTube, Facebook |
| Promo Video 1 (9:16) | `Videos/Bluebullfly Video 1 9_16.mp4` | Instagram Reels, TikTok |
| Promo Video 2 (16:9) | `Videos/Bluebullfly Video 2 16_9.mp4` | YouTube, Facebook |
| Promo Video 2 (9:16) | `Videos/Bluebullfly Video 2 9_16.mp4` | Instagram Reels, TikTok |

> **Quickest win**: Upload `Ad 1.png` or `Video 1 9_16.mp4` with a caption via Blotato right now — no AI generation needed!

---

## Notes

- All costs shown before any generation happens — you always approve first
- The brand file at `references/bluebullfly_BRAND.md` is your brand's "memory" — the agent reads it for every task
- Product images are already on Shopify CDN — no need to re-upload for reference
