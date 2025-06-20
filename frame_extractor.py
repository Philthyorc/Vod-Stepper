# vod_stepper/frame_extractor.py

import os
import cv2

def extract_frames(video_path: str, output_dir: str, fps: int = 2):
    """Extracts frames at precise intervals (e.g., every 0.5s) and saves them as PNGs."""
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Failed to open video: {video_path}")

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / video_fps
    interval_ms = 1000 / fps  # milliseconds per frame

    print(f"🎞 Extracting frames every {interval_ms:.0f}ms from: {video_path}")
    
    timestamp = 0.0
    count = 0

    while timestamp < duration * 1000:
        cap.set(cv2.CAP_PROP_POS_MSEC, timestamp)
        success, frame = cap.read()
        if not success:
            break

        frame_filename = f"frame_{count:04d}.png"
        frame_path = os.path.join(output_dir, frame_filename)
        cv2.imwrite(frame_path, frame)

        timestamp += interval_ms
        count += 1

    cap.release()
    print(f"✅ Saved {count} frames to: {output_dir}")
