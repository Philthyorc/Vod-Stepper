# vod_stepper/frame_extractor.py

import os
import cv2

def extract_frames(video_path: str, output_dir: str, fps: int = 1):
    """Extracts 1 FPS frames from the video and saves them as PNGs."""
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Failed to open video: {video_path}")

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(video_fps / fps)

    count = 0
    saved = 0

    print(f"🎞 Extracting frames from: {video_path}")
    while True:
        success, frame = cap.read()
        if not success:
            break

        if count % frame_interval == 0:
            frame_filename = f"frame_{saved:04d}.png"
            frame_path = os.path.join(output_dir, frame_filename)
            cv2.imwrite(frame_path, frame)
            saved += 1

        count += 1

    cap.release()
    print(f"✅ Saved {saved} frames to: {output_dir}")
