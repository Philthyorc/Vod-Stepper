# vod_stepper/downloader.py

import os
import subprocess
import uuid

def download_video(url: str) -> str:
    """Downloads a video using yt-dlp and returns the local file path."""

    # Step 1: Get title
    try:
        title_result = subprocess.run(
            ["yt-dlp", "--print", "title", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        video_title = title_result.stdout.strip()
    except Exception:
        video_title = "unknown_video"

    print(f"🎬 Title: {video_title}")

    # Step 2: Prepare filename and path
    safe_title = "".join(c for c in video_title if c.isalnum() or c in " _-").rstrip()
    output_dir = "temp_videos"
    os.makedirs(output_dir, exist_ok=True)
    video_filename = f"{safe_title}.mp4"
    video_path = os.path.join(output_dir, video_filename)

    # Step 3: Download the video
    command = [
        "yt-dlp",
        "-f", "best[ext=mp4]",
        "-o", video_path,
        url
    ]

    print(f"⬇️ Downloading video to: {video_path}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print("❌ yt-dlp failed with the following error:")
        print(result.stderr)
        raise RuntimeError(f"yt-dlp error:\n{result.stderr}")

    return video_path
