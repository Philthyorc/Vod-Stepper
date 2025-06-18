from flask import Flask, request, jsonify
from downloader import download_video
from frame_extractor import extract_frames
from on_point_detector import analyze_frames
import os

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        url = data.get("url")

        video_path = download_video(url)
        run_id = os.path.splitext(os.path.basename(video_path))[0]
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
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
