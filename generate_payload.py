import base64, json, os

file_paths = [
    "/Users/leo/Leo/Bulhoes.org/Marketing Bot/ad-creation/assets/Ad First Scene.png", 
    "/Users/leo/Leo/Bulhoes.org/Marketing Bot/ad-creation/assets/Logo.png",
    "/Users/leo/Leo/Bulhoes.org/Marketing Bot/ad-creation/assets/Bluebullfly_Fun.mp3",
    "/Users/leo/Leo/Bulhoes.org/Marketing Bot/ad-creation/assets/products/kids_cotton_tee_front.jpg"
] 

payload = {}
for path in file_paths:
    filename = os.path.basename(path)
    with open(path, "rb") as file:
        mime = "audio/mpeg" if path.endswith(".mp3") else "image/png" if path.endswith(".png") else "image/jpeg"
        encoded = base64.b64encode(file.read()).decode("utf-8")
        payload[filename] = f"data:{mime};base64,{encoded}"

html = f"""
<!DOCTYPE html>
<html><body><script>
    window.name = JSON.stringify({json.dumps(payload)});
    document.body.innerHTML = "DONE!";
</script></body></html>
"""

payload_path = "/Users/leo/Leo/Bulhoes.org/Marketing Bot/ad-creation/20260228-1908/payload_slice1.html"
with open(payload_path, "w") as f: 
    f.write(html)
