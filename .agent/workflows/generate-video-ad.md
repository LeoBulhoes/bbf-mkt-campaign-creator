---
description: Create a 30s marketing video ad using Gemini Veo 
agent: /Users/leo/Leo/Bulhoes.org/Marketing Bot/.agent/agents/Video Ad Director/instructions.md
---

# Workflow: Video Ad Generation via Gemini Veo

This workflow automates the creation of a 30-second promotional YouTube ad by generating four 8-second slices using Gemini Veo and stitching them together with FFmpeg. The workflow relies on automating Google Gemini's web interface via Javascript injection.

## Execution Rules
1. **Directory Structure:** For every new ad generation, create a new folder named with the current time in the format `yyyymmdd-hhmm` under `ad-creation/sessions/`. All generated slices and the final video must be stored here.
2. **Agent Directives:** Always strictly adhere to the constraints defined in your `instructions.md` file (Mascot integrity, continuity, etc.) and construct prompts using `prompt_templates.md`.

## Execution Steps

// turbo
1. Create a timestamped folder `yyyymmdd-hhmm` inside `ad-creation/sessions/`.

2. **Phase 1: Creative Direction & Prompt Validation [USER APPROVAL REQUIRED]**
   - **Product Selection:** If the user did not specify which products to use in the ad, pick at least two random image files from `/ad-creation/assets/products/` to use as references.
   - **Scene Script Generation:** Draft an overarching script/storyboard for the entire 30s ad using **hard cuts/stylized transitions** between the 8-second slices. The script MUST follow this strict 4-part narrative structure:
     - **Slice 1 (The Hook & Problem):** Grab attention immediately. **MUST include a visual or narrative hook within the first 5 seconds** (optimized for YouTube/Shorts ad retention). Introduce a relatable pain point or dull situation.
     - **Slice 2 (The Solution):** Introduce the brand/product as the catalyst for energy and resolution.
     - **Slice 3 (Benefits/Social Proof):** Show the emotional result (joy, active lifestyle, social engagement).
     - **Slice 4 (The Call to Action):** Drive the narrative to a clear resolution and a final graphic/logo freeze-frame.
     
     For each of these slices, you MUST explicitly define:
     - **Narrative Goal:** (e.g., "Establish the pain point of boredom")
     - **Shot Context:** (e.g., "Wide establishing shot", "Extreme close-up")
     - **Apparel/Props in Scene:** (Explicit tie to the exact reference images)
     - **Cut/Transition In:** (How this slice begins, e.g., "Hard cut to", "Whip-pan reveal")
     - **Action & Pacing:** (What the subjects are doing and the energy of the motion)
     - **End State (The Setup):** (Where the shot lands at the 8s mark, setting up the rhythm for the next cut)
   - **Prompt Validation:** Present the drafted Scene Script first. Then, referencing `prompt_templates.md`, present exactly what prompts will be executed for each slice, along with the list of assets that will be injected for each.
   - **Action:** Ask the user to review the entire plan. **DO NOT AUTO-PROCEED.** Wait for the user's explicit written approval.

3. **Phase 2: Generate Slice 1 (0s - 8s) [USER APPROVAL REQUIRED]**
   - Launch the `browser_subagent` to navigate to Gemini.
   - Upload via JS Injection: `Ad First Scene.png`, `Logo.png` (this is our mascot), `Bluebullfly_Fun.mp3`, and the selected product references.
   - **Prompt:** Construct the prompt using the **Slice 1** template from `prompt_templates.md` and applying all constraints from your agent instructions.
   - Download the generated video and move it to the timestamped folder as `slice1.mp4`.
   - **Action:** Ask the user to review `slice1.mp4`. **DO NOT AUTO-PROCEED.** Wait for the user's explicit written approval before extracting frames or continuing to Slice 2.

4. **Phase 3: Generate Slice 2 (8s - 16s)**
   // turbo
   - Extract the last frame: `ffmpeg -sseof -0.1 -i slice1.mp4 -vframes 1 -q:v 2 slice1_end.png`
   - Launch subagent and upload `slice1_end.png`, `Bluebullfly Text.png`, `Logo.png` (the mascot), `Bluebullfly_Fun.mp3`, and the **selected product references**.
   - **Prompt:** Construct the prompt using the **Slice 2** template from `prompt_templates.md` and applying all constraints from your agent instructions.
   - Download the generated video and move to the timestamped folder as `slice2.mp4`.

5. **Phase 4: Generate Slice 3 (16s - 24s)**
   // turbo
   - Extract the last frame: `ffmpeg -sseof -0.1 -i slice2.mp4 -vframes 1 -q:v 2 slice2_end.png`
   - Launch subagent and upload `slice2_end.png`, `Ad Backgrond.png`, `Bluebullfly_Fun.mp3`, and the **selected product references**.
   - **Prompt:** Construct the prompt using the **Slice 3** template from `prompt_templates.md` and applying all constraints from your agent instructions.
   - Download as `slice3.mp4`.

6. **Phase 5: Generate Slice 4 (24s - 32s)**
   // turbo
   - Extract the last frame: `ffmpeg -sseof -0.1 -i slice3.mp4 -vframes 1 -q:v 2 slice3_end.png`
   - Launch subagent and upload `slice3_end.png`, `Ad Last Scene.png`, and `Bluebullfly_Fun.mp3`.
   - **Prompt:** Construct the prompt using the **Slice 4** template from `prompt_templates.md` and applying all constraints from your agent instructions.
   - Download as `slice4.mp4`.

6. **Phase 5: Final Assembly**
   // turbo-all
   - Concatenate Slices 1-4 using FFmpeg into a raw video file.
   - Trim exactly to 30.0 seconds.
   - Sync and overlay the master `Bluebullfly_Fun.mp3` audio track track over the entire video, replacing the Veo generated audio completely.
   - Save the finalized video as `final_ad.mp4` in the timestamped folder.

## Technical Execution
To bypass `file://` restrictions and correctly upload image/audio files directly into `gemini.google.com` seamlessly with the browser_subagent:

Follow the steps outlined in the `.agent/skills/gemini_web_injection/SKILL.md` file.
