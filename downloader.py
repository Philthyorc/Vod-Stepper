# vod_stepper/downloader.py

import os
import subprocess
import uuid

def download_video(url: str) -> str:
    """Downloads a video using yt-dlp and returns the local file path."""
    output_dir = "temp_videos"
    os.makedirs(output_dir, exist_ok=True)

    video_filename = f"{uuid.uuid4().hex}.mp4"
    video_path = os.path.join(output_dir, video_filename)

    command = [
        "yt-dlp",
        "--cookies", "youtube_cookies.txt",
        "-f", "best[ext=mp4]",
        "-o", video_path,
        url
    ]

    print(f"⬇️ Downloading video to: {video_path}")

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print("❌ yt-dlp failed with the following error:")
        print(result.stderr)
        raise RuntimeError(f"yt-dlp error:\n{result.stderr}")

    return video_path
