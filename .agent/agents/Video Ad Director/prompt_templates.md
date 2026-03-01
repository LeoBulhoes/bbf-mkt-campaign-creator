# Veo Prompt Templates

The 30-second ad is divided into four 8-second slices. Use these exact base templates when generating prompts, filling in the bracketed information based on the overarching script.

## Slice 1 (0s - 8s) - The Hook & The Problem
**Required Assets:** `Ad First Scene.png`, `Logo.png`, `Bluebullfly_Fun.mp3`, Product References
**Template:**
"Create a video 16:9 aspect ratio. I attached the 1st scene image, our brand icon (a butterfly), some product references, and the song file. 
[Insert Slice 1 Action: The Hook and the Problem]. The models cannot be the focal point of the video. Sync the initial movements to the rhythm of the attached song. 
Style: Starts muted and dreary, transitioning to vibrant, high-contrast, glowing colors once the [Trigger Event/Butterfly] appears. 
Constraints: The brand icon cannot behave differently from a regular butterfly. Do not add any elements to the provided brand icon. Do not add a body or legs to the brand icon. Do not add voices. The generated models and backgrounds must be completely new and different from the reference product images."

## Slice 2 (8s - 16s) - The Solution
**Required Assets:** `slice1_end.png`, `Bluebullfly Text.png`, `Logo.png`, `Bluebullfly_Fun.mp3`, Product References
**Template:**
"Create a video 16:9 aspect ratio. I attached the starting scene image, our brand text, the brand icon (a butterfly), the song file, and the product references.
Context: Up to this point, [Summarize Ad Context up to Slice 1]. The attached starting scene image is the exact frame we left off on.
Action: HARD CUT to [Insert Slice 2 Action: The Solution and Transition].
Style: Realistic outdoor photography combining with 2D glowing cartoon butterfly. Ensure the apparel worn by the subjects remains consistent with Context and the references.
Constraints: The brand icon cannot behave differently from a regular butterfly. Do not add a body or legs to the brand icon. Do not add voices. Do not copy the reference product models directly."

## Slice 3 (16s - 24s) - The Benefits & Brand Energy
**Required Assets:** `slice2_end.png`, `Ad Background.png`, `Bluebullfly_Fun.mp3`, Product References
**Template:**
"Create a video 16:9 aspect ratio. I attached the starting scene image, the background environment, product references, and the song file.
Context: Up to this point, [Summarize Ad Context up to Slice 2]. The attached starting scene image is the exact frame we left off on.
Action: HARD CUT to [Insert Slice 3 Action: The Benefits and High Energy Movement].
Style: Dynamic camera movement, bright sunny outdoor lighting with the 2D glowing cartoon butterfly.
Constraints: The brand icon cannot behave differently from a regular butterfly. Do not add a body or legs to the brand icon. Do not add voices."

## Slice 4 (24s - 32s) - The CTA (Call to Action)
**Required Assets:** `slice3_end.png`, `Ad Last Scene.png`, `Bluebullfly_Fun.mp3`
**Template:**
"Create a video 16:9 aspect ratio. I attached the starting scene image, the final scene image, and the song file.
Context: Up to this point, [Summarize Ad Context up to Slice 3]. The attached starting scene image is the exact frame we left off on.
Action: HARD CUT to [Insert Slice 4 Action: The Final Resolution and CTA Setup leading into a graphic].
Style: Photorealistic transitioning into a final graphic freeze-frame of the brand icon.
Constraints: The brand icon cannot behave differently from a regular butterfly. Do not add a body or legs to the brand icon. Do not add voices."
