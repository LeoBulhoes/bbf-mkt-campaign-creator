---
name: Gemini Web Video Generation Payload Injection
description: How to correctly inject local files (images, audio) into the Gemini Web UI using a local HTML payload to bypass file:// restrictions and automate video generation.
---

# Skill: Gemini Web Payload Injection

When automating the Gemini Web interface (`https://gemini.google.com`) using a browser subagent, you cannot directly read local `file://` URLs in the page context, nor can you easily upload multiple files via standard browser UI interactions reliably for complex payloads (like mixing audio and multiple images).

To solve this, use the **HTML Payload Injection Method**.

## Execution Steps

### 1. Generate `payload.html` Locally
Before launching the browser subagent, run a local Python script to read the necessary files, convert them to base64, and output an HTML file.

```python
import base64, json, os

# 1. Define the absolute paths to the files you need to upload
file_paths = [
    "/absolute/path/to/image.png", 
    "/absolute/path/to/audio.mp3"
] 

payload = {}
for path in file_paths:
    filename = os.path.basename(path)
    with open(path, "rb") as file:
        mime = "audio/mpeg" if path.endswith(".mp3") else "image/png" # Adjust MIME as needed
        encoded = base64.b64encode(file.read()).decode("utf-8")
        payload[filename] = f"data:{mime};base64,{encoded}"

# 2. Construct the HTML that writes to window.name
html = f"""
<!DOCTYPE html>
<html><body><script>
    window.name = JSON.stringify({json.dumps(payload)});
    document.body.innerHTML = "DONE!";
</script></body></html>
"""

# 3. Save the payload file somewhere the browser can access
payload_path = "/absolute/path/to/workspace/assets/payload.html"
with open(payload_path, "w") as f: 
    f.write(html)
```

### 2. Browser Subagent Execution
Once `payload.html` is created, instruct your browser subagent to execute the following exact sequence:

1. **Navigate to the local payload:** Navigate to the `file://` URL of the generated `payload.html` (e.g., `file:///absolute/path/to/workspace/assets/payload.html`).
2. **Wait for confirmation:** Wait until the body text displays "DONE!". This confirms the base64 data is loaded into the tab's `window.name` property.
3. **Navigate to Gemini:** **In the exact same tab**, navigate to `https://gemini.google.com/`. Wait for the page to fully load.
4. **Inject the Payload:** Run the following `execute_browser_javascript` snippet to retrieve the stored data from `window.name` and paste it directly into Gemini's input area:

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

5. **Type the Prompt:** After the files are pasted, use the standard browser typing tools to enter the text prompt and submit.
