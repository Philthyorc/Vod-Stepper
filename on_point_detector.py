# vod_stepper/on_point_detector.py

import os
import cv2
import numpy as np
from typing import Dict, List

def analyze_frames(frames_dir: str) -> Dict:
    results: List[Dict] = []
    frame_files = sorted(f for f in os.listdir(frames_dir) if f.endswith('.png'))

    print(f"🔍 Analyzing {len(frame_files)} frames...")

    for idx, filename in enumerate(frame_files):
        frame_path = os.path.join(frames_dir, filename)
        frame = cv2.imread(frame_path)

        if frame is None:
            print(f"⚠️ Skipped unreadable frame: {filename}")
            continue

        h, w = frame.shape[:2]
        center_x, center_y = w // 2, h // 2
        radius = 120  # size of circle around the flag to scan

        # Create a circular mask centered on screen
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (center_x, center_y), radius, 255, thickness=-1)

        # Convert to HSV and apply color mask
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Red mask: includes low and high hue range
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([179, 255, 255])
        red_mask = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)

        # Blue mask
        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([130, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Combine and apply mask to center ring
        combined_mask = cv2.bitwise_or(red_mask, blue_mask)
        masked_area = cv2.bitwise_and(combined_mask, combined_mask, mask=mask)

        # Count how much of the circular area is red or blue
        pixel_count = cv2.countNonZero(masked_area)
        total_circle_pixels = cv2.countNonZero(mask)
        coverage_ratio = pixel_count / total_circle_pixels if total_circle_pixels > 0 else 0

        on_point = coverage_ratio > 0.05  # 5% of ring must be red or blue

        results.append({
            "frame": filename,
            "second": idx,
            "on_point": on_point
        })

    return {
        "summary": {
            "total_frames": len(results),
            "total_seconds": len(results),
            "on_point_seconds": sum(1 for r in results if r["on_point"])
        },
        "details": results
    }
