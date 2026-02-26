# Prompt Best Practices — Image & Video Generation

Guide for writing prompts that produce high-quality marketing content with accurate product representation of the image included.

---

## Golden Rule: Keep It Simple

> [!IMPORTANT]
> **Simpler prompts produce better product accuracy.** Over-describing the product confuses the AI model. Instead, let the reference images do the heavy lifting and keep your text prompt focused on the **scene, setting, and action**.

**Best prompt pattern:**
```
[Aspect Ratio]. [Scene naturally referencing "this [product type]"]. [Optional mood/lighting].
```

The word **"this"** tells the AI to use the attached reference image as the product. Embed **"this t-shirt"**, **"this hoodie"**, **"this cap"** etc. naturally in the sentence.

**Example — Great (natural embedding):**
```
9:16. Create a picture of a child playing on a playground wearing this t-shirt.
```

**Example — Bad (over-described):**
```
9:16. A 6-year-old child wearing the Bluebullfly Kids Cotton T-Shirt with an all-over
repeating pattern of blue cartoon butterflies with yellow smiley faces, each butterfly
has 4 rounded blue wings... DO NOT MODIFY THE SHIRT DESIGN...
```

The simple version produces **more accurate** product reproduction because the AI focuses on matching the reference image rather than trying to interpret a complex text description.

---

## 1. Image Prompts (Nano Banana / Nano Banana Pro)

### Structure

Every image prompt should follow this order:

```
[Aspect Ratio]. [Scene naturally referencing "this [product]"]. [Optional mood/lighting].
```

**Examples:**
```
9:16. Create a picture of a child playing on a playground wearing this t-shirt.
```
```
4:5. An aesthetic flat-lay overhead shot on a rustic wooden table featuring this cap, this mug, and this sticker. Warm sunbeams.
```
```
9:16. A young man in a dark bedroom mirror selfie wearing this hoodie.
```

### Aspect Ratio (ALWAYS First)

Start every prompt with the aspect ratio followed by a period:
- `9:16.` — Vertical (Instagram Reels, TikTok, YouTube Shorts, Stories)
- `4:5.` — Portrait (Instagram Feed, LinkedIn)
- `1:1.` — Square (Instagram Feed, Twitter)
- `16:9.` — Landscape (YouTube, website banners)
- `3:4.` — Tall portrait (Pinterest)

### Reference Images

Always attach the **product photo** (not the logo) as the reference image. The prompt should reference it naturally using **"this [product type]"**.

> [!TIP]
> Do NOT describe product details (colors, patterns, logos) in the text prompt. The reference image already contains all that information. Adding text descriptions of the product **conflicts** with the reference and produces worse results.

### Subject Description

Be specific about the person:
- **Age range**: "early 20s", "late 30s"
- **Style/vibe**: "streetwear", "minimalist", "athleisure"
- **Body language**: "relaxed lean", "power stance", "mid-stride", "looking over shoulder"
- **Facial expression**: "subtle smirk", "focused determination", "genuine laugh"

### Image Types & Their Prompts

#### UGC / Selfie Style (~30% of campaign)
```
9:16. A young woman filming herself in a bathroom mirror wearing this t-shirt,
phone visible in frame, authentic social media aesthetic.
```

**Tips:**
- Include the phone in the shot
- Natural/imperfect lighting (ring lights, window light)
- Slightly messy, real environments
- Eye contact with camera

#### Studio Hero Shot (~25% of campaign)
```
9:16. Male model standing on grey concrete floor wearing this hoodie, full body shot,
dramatic moody lighting.
```

**Tips:**
- Clean, minimal backdrops (grey, concrete, white)
- Dramatic lighting (side-lit, rim-lit, high-contrast)
- Strong poses (power stance, hands in pockets, looking away)

#### Close-up Detail (~15% of campaign)
```
4:5. Close-up detail shot of this t-shirt focusing on fabric and stitching,
shallow depth of field.
```

**Tips:**
- Specify which detail: zipper, stitching, hardware, logo, fabric texture
- Use "shallow depth of field" and "macro" keywords
- 4:5 or 1:1 ratios work best for detail shots

#### Urban Lifestyle (~15% of campaign)
```
9:16. Young man walking through a city street wearing this t-shirt,
candid street photography.
```

**Tips:**
- Gritty urban settings: parking garages, alleys, rooftops, subway stations
- Motion blur adds dynamism
- Neon/fluorescent/street lights for mood

#### CGI / World-Building (~10% of campaign)
```
9:16. This t-shirt displayed on a mannequin in a futuristic setting,
volumetric lighting, cinematic render.
```

**Tips:**
- Use "render", "CGI", "3D", "volumetric lighting" for quality cues
- Match the brand aesthetic (cyberpunk, minimal, brutalist)
- Product can be on a mannequin or floating

#### Flat Lay / Product (~5% of campaign)
```
4:5. Flat-lay overhead shot of this t-shirt on a rustic wooden table, warm sunbeams.
```

**Tips:**
- Overhead angle always
- Complementary accessories that match the brand
- Clean, textured surfaces (marble, wood, concrete, slate)

### Lighting Keywords

| Keyword | Effect |
|---------|--------|
| "natural lighting" | Soft, authentic, outdoor feel |
| "golden hour" | Warm, flattering, sunset tones |
| "moody lighting" | Dark, dramatic, high contrast |
| "studio lighting" | Clean, professional, even |
| "neon glow" | Colorful, urban, nightlife |
| "rim lighting" | Edge-lit silhouette, dramatic |
| "overhead fluorescent" | Industrial, gritty, green tint |
| "LED backlighting" | Modern, tech-forward, colorful |

### Emotional Direction

Always include emotional context:
- "excited energy" — jumping, laughing, animated gestures
- "calm confidence" — relaxed pose, steady gaze, minimal movement
- "mysterious" — turned away, shadows on face, looking down
- "casual cool" — one hand in pocket, slight smirk
- "powerful" — wide stance, arms crossed, direct eye contact

---

## 2. Video Prompts (Veo 3.1)

### Structure

```
[Motion Description]. [Camera Movement]. [Atmosphere/Mood].
```

**Example:**
```
Starting from the image, the person slowly turns toward the camera with a confident smirk.
Slow push-in camera movement. Moody atmosphere with subtle lens flare.
```

### Key Principles

1. **Reference the source image**: Always start with "Starting from the image..." so Veo knows to animate from the Generated Image
2. **Subtle motion wins**: Veo produces better results with controlled, intentional movement rather than chaotic action
3. **Describe what CHANGES**: Don't re-describe the static scene — describe what moves
4. **Camera movement matters**: Specify one clear camera motion

### Camera Movement Keywords

| Keyword | Effect |
|---------|--------|
| "slow push-in" | Slowly zooming toward subject — builds intensity |
| "dolly zoom" | Subject stays same size while background shifts — dramatic |
| "orbit / arc" | Camera circles around subject — reveals product from angles |
| "handheld tracking" | Follows subject walking — casual, documentary feel |
| "static / locked off" | Camera doesn't move — focus on subject's movement |
| "tilt up" | Camera pans from feet to head — dramatic reveal |
| "pull back" | Camera moves away — reveals environment |

### Duration Guidelines

| Duration | Best For |
|----------|----------|
| 4 seconds | Quick hooks, single motion, detail shots |
| 6 seconds | Standard reveal, turn + pose, walk-and-stop |
| 8 seconds | Full scene, walk + pause + turn, multi-motion |

### Video Prompt Examples by Type

#### Product Reveal (4s)
```
Starting from the image, the t-shirt slowly rotates on the mannequin.
Camera doing a gentle orbit. Studio spotlights creating dynamic shadows.
```

#### UGC Style (6s)
```
Starting from the image, the person raises their phone for a selfie video,
gives a slight nod to camera. Handheld camera feel with slight shake.
```

#### Lifestyle Walk (8s)
```
Starting from the image, the person pushes off the wall and walks toward
the camera. Slow tracking shot following their stride.
```

#### Dramatic Hero (6s)
```
Starting from the image, wind begins blowing the fabric.
The person slowly looks up toward the camera with intense eye contact.
Slow push-in. Cinematic lens flare from the right.
```

---

## 3. Model-Specific Tips

### Nano Banana Pro (Images)
- **Keep prompts short** — simpler prompts produce better product accuracy
- Reference the product naturally: **"this t-shirt"**, **"this hoodie"**, etc.
- Do NOT describe product details in text — let the reference image do the work
- 9:16 and 4:5 produce the sharpest results
- Struggles with readable text/brand names — avoid requesting text overlays

### Veo 3.1 (Videos)
- Image-to-video produces more consistent results than text-to-video
- Best motion: hair/fabric blowing, slow turns, walking, subtle gestures
- Avoid: fast action, complex multi-person scenes, precise hand movements
- Always generate the image first, approve it, THEN generate the video from it
- Videos are ~$0.50 each — be selective about which posts get video

---

## 4. Campaign Consistency

- Use the same reference images across all prompts for product consistency
- Reference the product naturally with **"this [product]"** in every prompt
- Vary **settings, lighting, and action** — NOT the product appearance
- Mix indoor/outdoor settings for variety
