# vod_stepper/main.py

import os
import shutil
import time
from downloader import download_video
from frame_extractor import extract_frames
from on_point_detector import analyze_frames
from utils import save_report, format_duration

def main():
    # Step 1/4: Download video
    print("📥 Step 1/4: Downloading video...")
    vod_url = input("Enter YouTube VOD URL: ")

    try:
        video_path = download_video(vod_url)
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return

    # Step 2/4: Extract frames
    print("🧪 Step 2/4: Extracting frames...")
    frames_dir = os.path.join("output", "frames")
    fps = 2  # 0.5 seconds per frame
    extract_frames(video_path, frames_dir, fps=fps)

    # Step 3/4: Analyze frames
    print("🧠 Step 3/4: Analyzing frames...")
    report_data = analyze_frames(frames_dir, fps=fps, verbose=False)

    # Step 4/4: Save report and cleanup
    print("📦 Step 4/4: Saving report and cleaning up...")
    save_report(report_data, os.path.join("output", "report.json"))

    # Summary
    total = report_data["summary"]["total_seconds"]
    on_point = report_data["summary"]["on_point_seconds"]
    pct = (on_point / total) * 100 if total > 0 else 0

    print("\n🎯 Summary")
    print(f"⏱️  Total Duration: {format_duration(int(total))}")
    print(f"🛡️  On Point: {format_duration(int(on_point))} ({pct:.1f}%)")
    print(f"📁 Report saved to: output/report.json")

    # Clean up video file
    try:
        os.remove(video_path)
        print(f"🧹 Deleted video: {video_path}")
    except Exception as e:
        print(f"⚠️ Could not delete video: {e}")

    # Delay before trying to delete frames (to prevent file lock errors)
    time.sleep(1)

    # Clean up frames folder
    try:
        shutil.rmtree(frames_dir)
        print(f"🧹 Deleted frames directory: {frames_dir}")
    except Exception as e:
        print(f"⚠️ Could not delete frames — folder may still be open or locked.\n{e}")

if __name__ == "__main__":
    main()
