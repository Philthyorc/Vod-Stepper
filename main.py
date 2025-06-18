# vod_stepper/main.py

import os
from downloader import download_video
from frame_extractor import extract_frames
from on_point_detector import analyze_frames
from utils import save_report, format_duration  # 🆕 added format_duration

def main():
    # Step 1: Download VOD
    vod_url = input("Enter VOD URL: ")
    video_path = download_video(vod_url)

    # Step 2: Extract 1 FPS frames from video
    frames_dir = os.path.join("output", "frames")
    extract_frames(video_path, frames_dir, fps=1)

    # Step 3: Analyze frames for on-point detection
    report_data = analyze_frames(frames_dir)

    # Step 4: Save report
    save_report(report_data, os.path.join("output", "report.json"))

    # 🆕 Step 5: Print readable summary
    total = report_data["summary"]["total_seconds"]
    on_point = report_data["summary"]["on_point_seconds"]
    pct = (on_point / total) * 100 if total > 0 else 0

    print("\n🎯 Summary")
    print(f"⏱️  Total Duration: {format_duration(total)}")
    print(f"🛡️  On Point: {format_duration(on_point)} ({pct:.1f}%)")
    print(f"📁 Report saved to: output/report.json")

if __name__ == "__main__":
    main()
