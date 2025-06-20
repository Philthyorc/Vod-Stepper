# vod_stepper/on_point_detector.py

import os
import cv2
import numpy as np
from typing import Dict, List
from math import sqrt

def analyze_frames(frames_dir: str, fps: int = 2, verbose: bool = False) -> Dict:
    results: List[Dict] = []
    frame_files = sorted(f for f in os.listdir(frames_dir) if f.endswith('.png'))

    print(f"🔍 Analyzing {len(frame_files)} frames...")

    for idx, filename in enumerate(frame_files):
        frame_path = os.path.join(frames_dir, filename)
        frame = cv2.imread(frame_path)

        if frame is None:
            if verbose:
                print(f"⚠️ Skipped unreadable frame: {filename}")
            continue

        h, w = frame.shape[:2]
        center_x = w // 2
        feet_y = int(h * 0.75)
        flag_y = h // 2

        # Distance from feet to flag center
        distance_to_flag = sqrt((center_x - center_x) ** 2 + (feet_y - flag_y) ** 2)

        # Require feet to be within 100px of flag center
        proximity_ok = distance_to_flag < 100

        # Build flag mask (same as before)
        flag_radius = 130
        mask_flag = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask_flag, (center_x, flag_y), flag_radius, 255, thickness=-1)

        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Tighter red
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([5, 255, 255])
        lower_red2 = np.array([170, 100, 100])
        upper_red2 = np.array([179, 255, 255])
        red_mask = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)

        # Tighter blue
        lower_blue = np.array([110, 100, 100])
        upper_blue = np.array([125, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        combined_mask = cv2.bitwise_or(red_mask, blue_mask)
        masked_flag = cv2.bitwise_and(combined_mask, combined_mask, mask=mask_flag)

        pixel_flag = cv2.countNonZero(masked_flag)
        total_flag = cv2.countNonZero(mask_flag)
        coverage_flag = pixel_flag / total_flag if total_flag > 0 else 0

        # Final check: must be near flag AND flag zone must be active
        threshold = 0.035
        on_point = proximity_ok and coverage_flag > threshold

        if verbose:
            print(f"{filename}: dist={distance_to_flag:.1f}, flag_coverage={coverage_flag:.3f} → {'ON' if on_point else 'off'}")

        results.append({
            "frame": filename,
            "second": round(idx / fps, 2),
            "on_point": on_point
        })

    return {
        "summary": {
            "total_frames": len(results),
            "total_seconds": round(len(results) / fps, 2),
            "on_point_seconds": round(sum(1 for r in results if r["on_point"]) / fps, 2)
        },
        "details": results
    }
