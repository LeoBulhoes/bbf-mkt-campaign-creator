import sys
import os

from dotenv import load_dotenv
load_dotenv('references/.env')

import google.generativeai as genai

genai.configure(api_key=os.environ.get("GOOGLE_AISTUDIO_API_KEY"))

with open(".agent/workflows/art-director.md", "r") as f:
    art_director_prompt = f.read()

with open("/Users/leo/.gemini/antigravity/brain/2a2dd4c5-809c-417a-ae21-8fcd2880600d/prompt_plan.md", "r") as f:
    prompt_plan = f.read()

model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content(
    f"System Prompt: {art_director_prompt}\n\nUser Plan: {prompt_plan}"
)

print(response.text)
