# Blubullfly: Master Prompting Guide (Nano Banana Pro & Veo 3.1)
**Goal:** High-accuracy product representation for mass-market North American sales.

---

## 🏆 The Golden Rule: Reference, Don't Describe
**Never describe colors, patterns, or logos of the product in text.** The AI uses the attached reference image for those details. Describing them in the prompt creates "Prompt Leakage," leading to design errors.

**The Magic Phrase:** Always use **"this [product category]"** (e.g., "this t-shirt", "this hoodie"). This "locks" the AI onto the reference image.

### Product Categories 
* T-Shirt
* Hoodie
* Cap
* Mug
* Sticker


---

## 1. Image Generation (Nano Banana Pro)

### Prompt Structure
`[Aspect Ratio]. [Scene naturally referencing "this product category"]. [Subject Details]. [Lighting/Mood].`

### Step 1: Aspect Ratio (Must be first)
* `9:16.` — Vertical (TikTok, Reels, Shorts)
* `4:5.` — Portrait (Instagram/Facebook Feed)
* `1:1.` — Square (Standard Feed)
* `16:9.` — Landscape (Website banners)

### Step 2: High-Volume Scene Templates
| Style | Prompt Formula |
| :--- | :--- |
| **UGC/Selfie** | `A mirror selfie wearing this hoodie, clean bedroom background, authentic social media vibe.` |
| **Active Lifestyle**| `A child playing tag on a sunny playground wearing this t-shirt. Candid action shot.` |
| **Studio Hero** | `Professional model standing against a grey concrete wall wearing this hoodie. High-fashion pose.` |
| **Urban/Street** | `A teenager walking through a colorful city street wearing this t-shirt. Street photography.` |

---

## 2. Audience & Brand Guardrails (North America)

### 🌎 Diversity Logic (Canada/US Blend)
When generating a batch of images for a campaign, rotate the subject's ethnicity to match the North American market:
* **60% Caucasian** (e.g., "a person with fair skin")
* **20% Hispanic/Latino** (e.g., "a person with olive skin/Hispanic heritage")
* **15% Black/African American** (e.g., "a person with dark skin/African heritage")
* **5% Asian** (e.g., "a person with East Asian features")

### 🚫 Brand "No-Go" Zones
To maintain a high-end commercial feel, the agent must avoid:
* **Messy Environments:** No cluttered backgrounds or piles of clothes in "UGC" shots.
* **Competing Logos:** Ensure the background doesn't contain visible logos of other brands.
* **Complex Text:** Do not request text on the clothes or "SALE" signs; Nano Banana struggles with text.
* **Political/Religious Symbols:** Keep environments neutral (playgrounds, parks, clean studios, city streets).

---

## 3. Video Generation (Veo 3.1)

### The Two-Image Visual Anchor
For maximum accuracy, provide two visual inputs to the AI:
1. **The [ad]**: The approved Generated Image from Section 1 (serves as the starting frame).
2. **The [shop image]**: The original high-res product photo (serves as the detail reference).

### The "Product-First" Video Formula
`Starting from the [ad], the subject wearing **this [product]** [Motion Description]. [Camera Movement]. [Atmosphere].`

* **Rule:** Only describe the **CHANGE**. Do not re-describe the static scene of the [ad]; only describe what moves.
* **Rule:** Anchor to the product. Use "this [product]" to force the AI to map details from the shop image onto the video movement.

### Camera Movement Keywords
* **Slow push-in:** Builds focus on the product.
* **Orbit / Arc:** Circles the subject to reveal the product from different angles.
* **Handheld tracking:** Creates a casual, documentary/UGC feel.
* **Tilt up:** A dramatic reveal from feet to head.

---

## 4. Implementation Logic (Sets & Safety)
* **Product Consistency:** Use the exact same reference image for the Image and the Video for product consistency.
* **Multiple Products:** If a set is required in the future, reference both naturally: "A person wearing **this cap** and **this t-shirt**."
* **Environment Logic:** Ensure the background matches the item (e.g., no winter jackets on a beach).
* **Text:** Nano Banana struggles with text; do not ask for words like "SALE" or "NEW" on the clothes.
* **No-Go Zones:** Avoid messy rooms, political/religious symbols, or competing brand logos in backgrounds.