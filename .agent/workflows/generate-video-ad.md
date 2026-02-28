---
description: Create a 30s marketing video ad using Gemini Veo 
---

# Workflow: Video Ad Generation via Gemini Veo

This workflow automates the creation of a 30-second promotional YouTube ad by generating four 8-second slices using Gemini Veo and stitching them together with FFmpeg. The workflow relies on automating Google Gemini's web interface via Javascript injection.

## Rules & Constraints
1. **Directory Structure:** For every new ad generation, create a new folder named with the current time in the format `yyyymmdd-hhmm` under `ad-creation/`. All generated slices and the final video must be stored here.
2. **File Access Base:** The subagent can access the assets directly from the `file:///Users/leo/Leo/Bulhoes.org/Marketing%20Bot/ad-creation/assets/` directory URL in the browser, avoiding the need to open each file in a new tab to extract base64.
3. **Mascot/Logo Integrity:** Logo/mascot(butterfly) cannot be modified. It needs to behave like a butterfly if animated. Do not add body or legs to the mascot logo. The prompt must explicitly state: "Do not add any elements to the provided logo/mascot. Do not add a body or legs to the logo. Effects, transformations and transitions are okay to be added."
4. **No Voices:** The prompt must forbid voices: "Do not add any voices."
5. **Product & Environment References:** The generated backgrounds and models *must not* be identical to the reference pictures. The prompt must instruct: "Use the attached product as an inspiration for scenes and how produts look like, but the generated models and backgrounds must be completely new and different from the reference product images. Do not copy the reference models." 
6. **Continuation via Frames:** To ensure the scenes flow perfectly together, after each slice is generated, use `ffmpeg` to extract the *last frame* of the previous video and use that as the starting image for the next slice.

## Execution Steps

// turbo
1. Create a timestamped folder `yyyymmdd-hhmm` inside `ad-creation/`.

2. **Phase 1: Creative Direction & Prompt Validation [USER APPROVAL REQUIRED]**
   - **Product Selection:** If the user did not specify which products to use in the ad, pick at least two random image files from `/ad-creation/assets/products/` to use as references.
   - **Scene Script Generation:** Draft an overarching script/storyboard for the entire 30s ad, detailing the environment, character actions, and transitions across all 4 slices realistically so there is absolute continuity.
   - **Prompt Validation:** Present the drafted Scene Script first. Then present exactly what prompts will be executed for each slice (referencing their part in the overall script), along with the list of assets that will be injected for each.
   - **Action:** Ask the user to review the entire plan. **DO NOT AUTO-PROCEED.** Wait for the user's explicit written approval.

3. **Phase 2: Generate Slice 1 (0s - 8s) [USER APPROVAL REQUIRED]**
   - Launch the `browser_subagent` to navigate to Gemini.
   - Upload via JS Injection: `Ad First Scene.png`, `Logo.png` (this is our mascot), `Bluebullfly_Fun.mp3`, and the selected product references.
   - **Prompt Template:** "Create a video 16:9 aspect ratio. I attached the 1st scene image, our logo (which is the same entity as our mascot, a butterfly), some product references, and the song file. [Insert Slice 1 Action]. The models cannot be the focal point of the video. Sync the initial movements to the rhythm of the attached song. \n Style: Start 2D hand-drawn, thick charcoal outlines, transitioning to realistic bright outdoor photography. \n Constraints: The logo and mascot are the exact same entity. The mascot is a butterfly and cannot behave differently from a butterfly. Do not add any elements to the provided mascot. Do not add a body or legs to the mascot/logo. Do not add voices. The generated models and backgrounds must be completely new and different from the reference product images."
   - Download the generated video and move it to the timestamped folder as `slice1.mp4`.
   - **Action:** Ask the user to review `slice1.mp4`. **DO NOT AUTO-PROCEED.** Wait for the user's explicit written approval before extracting frames or continuing to Slice 2.

4. **Phase 3: Generate Slice 2 (8s - 16s)**
   // turbo
   - Extract the last frame: `ffmpeg -sseof -0.1 -i slice1.mp4 -vframes 1 -q:v 2 slice1_end.png`
   - Launch subagent and upload `slice1_end.png`, `Bluebullfly Text.png`, `Logo.png` (the mascot), `Bluebullfly_Fun.mp3`, and the **selected product references**.
   - **Prompt Template:** "Create a video 16:9 aspect ratio. I attached the starting scene image, our brand text, the logo (which is the same entity as our mascot, a butterfly), the song file, and the product references. \n\n Context: Up to this point, [Summarize Ad Context up to Slice 1]. The attached starting scene image is the exact frame we left off on. \n\n Action: [Insert Slice 2 Action dictating the transition from the starting frame to the new scene]. \n\n Style: Realistic outdoor photography combining with 2D hand-drawn cartoon mascot. Ensure the apparel worn by the teens remains consistent with Context and the references. \n Constraints: The logo and mascot are the exact same entity. The mascot is a butterfly and cannot behave differently from a butterfly. Do not add a body or legs to the mascot/logo. Do not add voices. Do not copy the reference product models directly."
   - Download the generated video and move to the timestamped folder as `slice2.mp4`.

5. **Phase 4: Generate Slice 3 (16s - 24s)**
   // turbo
   - Extract the last frame: `ffmpeg -sseof -0.1 -i slice2.mp4 -vframes 1 -q:v 2 slice2_end.png`
   - Launch subagent and upload `slice2_end.png`, `Ad Backgrond.png`, `Bluebullfly_Fun.mp3`, and the **selected product references**.
   - **Prompt Template:** "Create a video 16:9 aspect ratio. I attached the starting scene image, the background environment, product references, and the song file. \n\n Context: Up to this point, [Summarize Ad Context up to Slice 2]. The attached starting scene image is the exact frame we left off on. \n\n Action: [Insert Slice 3 Action dictating the transition from the starting frame to the new environment]. \n\n Style: Transitioning heavily into the 2D hand-drawn cartoon style of the background. \n Constraints: The mascot is a butterfly and cannot behave differently from a butterfly. Do not add a body or legs to the mascot/logo. Do not add voices."
   - Download as `slice3.mp4`.

6. **Phase 5: Generate Slice 4 (24s - 32s)**
   // turbo
   - Extract the last frame: `ffmpeg -sseof -0.1 -i slice3.mp4 -vframes 1 -q:v 2 slice3_end.png`
   - Launch subagent and upload `slice3_end.png`, `Ad Last Scene.png`, and `Bluebullfly_Fun.mp3`.
   - **Prompt Template:** "Create a video 16:9 aspect ratio. I attached the starting scene image, the final scene image, and the song file. \n\n Context: Up to this point, [Summarize Ad Context up to Slice 3]. The attached starting scene image is the exact frame we left off on. \n\n Action: [Insert Slice 4 Action dictating the seamless landing transition into the final scene]. \n\n Style: 2D hand-drawn cartoon. \n Constraints: The mascot is a butterfly and cannot behave differently from a butterfly. Do not add a body or legs to the mascot/logo. Do not add voices."
   - Download as `slice4.mp4`.

6. **Phase 5: Final Assembly**
   // turbo-all
   - Concatenate Slices 1-4 using FFmpeg into a raw video file.
   - Trim exactly to 30.0 seconds.
   - Sync and overlay the master `Bluebullfly_Fun.mp3` audio track track over the entire video, replacing the Veo generated audio completely.
   - Save the finalized video as `final_ad.mp4` in the timestamped folder.

## Technical Execution (Payload HTML Method)
To inject files into `https://gemini.google.com` without reading local `file://` URLs directly in the page context or running a local HTTP server, follow this fast process:

1. **Generate `payload.html` locally using Python:**
Before launching the subagent for a slice, run a local Python script to read the necessary files, convert them to base64, and output an HTML file to `ad-creation/assets/payload.html`. 

```python
import base64, json, os
# List of paths needed for the current slice
files = ["Logo.png", "Bluebullfly_Fun.mp3"] 
payload = {}
for f in files:
    path = os.path.join("ad-creation/assets", f)
    with open(path, "rb") as file:
        mime = "audio/mpeg" if path.endswith(".mp3") else "image/png"
        encoded = base64.b64encode(file.read()).decode("utf-8")
        payload[f] = f"data:{mime};base64,{encoded}"

html = f"""
<!DOCTYPE html>
<html><body><script>
    window.name = JSON.stringify({json.dumps(payload)});
    document.body.innerHTML = "DONE!";
</script></body></html>
"""
with open("ad-creation/assets/payload.html", "w") as f: f.write(html)
```

2. **Subagent Execution:**
- Launch the `browser_subagent`.
- Navigate to `file:///Users/leo/Leo/Bulhoes.org/Marketing%20Bot/ad-creation/assets/payload.html`.
- Wait until the body displays "DONE!". This loads the base64 data into the tab's `window.name`.
- **In the same exact tab**, navigate to `https://gemini.google.com/`. Wait for the page to load.
- Run the following `execute_browser_javascript` snippet to retrieve the stored data and paste it into the rich-textarea simultaneously:

```javascript
const data = JSON.parse(window.name);
const dt = new DataTransfer();

for (const [filename, dataurl] of Object.entries(data)) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while(n--){ u8arr[n] = bstr.charCodeAt(n); }
    dt.items.add(new File([u8arr], filename, {type:mime}));
}

const pasteEvent = new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true });
const inputArea = document.querySelector('rich-textarea');
if (inputArea) inputArea.dispatchEvent(pasteEvent);
```
