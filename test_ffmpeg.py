import imageio_ffmpeg
import subprocess
import os
import sys

# Generate a dummy video
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
os.system(f'"{ffmpeg}" -f lavfi -i color=c=blue:s=720x1280:d=1 -y test_in.mp4 >/dev/null 2>&1')

mask_path = "references/brands/bluebullfly/logo/Ad Mask.png"

cmd = [
    ffmpeg, "-y",
    "-i", "test_in.mp4",
    "-i", mask_path,
    "-filter_complex", "[1:v][0:v]scale2ref[mask][main];[main][mask]overlay=0:0",
    "test_out.mp4"
]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("FAILED")
    print(res.stderr)
else:
    print("SUCCESS")
