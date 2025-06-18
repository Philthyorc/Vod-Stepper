# vod_stepper/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid

from downloader import download_video
from frame_extractor import extract_frames
from on_point_detector import analyze_frames
from utils import save_report

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Generate unique ID for this request
        run_id = str(uuid.uuid4())
        video_path = download_video(url)
        frame_dir = os.path.join("output", "frames", run_id)
        os.makedirs(frame_dir, exist_ok=True)

        extract_frames(video_path, frame_dir, fps=1)
        report = analyze_frames(frame_dir)

        total = report["summary"]["total_seconds"]
        on_point = report["summary"]["on_point_seconds"]
        pct = (on_point / total) * 100 if total > 0 else 0

        return jsonify({
            "total_seconds": total,
            "on_point_seconds": on_point,
            "percentage": round(pct, 1)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
