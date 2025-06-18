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
        "-f", "best[ext=mp4]",
        "-o", video_path,
        url
    ]

    print(f"⬇️ Downloading video to: {video_path}")
    subprocess.run(command, check=True)

    return video_path
