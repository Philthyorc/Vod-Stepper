# vod_stepper/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import os
import shutil
import traceback

from downloader import download_video
from frame_extractor import extract_frames
from on_point_detector import analyze_frames

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return '''
        <h1>New World VOD Stepper</h1>
        <p>Paste a YouTube link in your local app to analyze how long you held point.</p>
        <p>This server is running correctly.</p>
    '''

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Extract and normalize video ID
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        return jsonify({'error': 'Invalid YouTube URL format'}), 400
    video_id = match.group(1)
    normalized_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        # Step 1: Download video
        video_path = download_video(normalized_url)

        # Step 2: Extract frames at 1 FPS
        frames_dir = os.path.join("temp_frames", video_id)
        extract_frames(video_path, frames_dir, fps=1)

        # Step 3: Analyze frames for on-point detection
        report = analyze_frames(frames_dir)

        # Step 4: Parse results
        total_seconds = report["summary"]["total_seconds"]
        on_point_seconds = report["summary"]["on_point_seconds"]
        percentage = round((on_point_seconds / total_seconds) * 100, 2) if total_seconds else 0.0

        return jsonify({
            'on_point_seconds': on_point_seconds,
            'total_seconds': total_seconds,
            'percentage': percentage
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

    finally:
        # Cleanup: remove temp video + frames
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(frames_dir):
            shutil.rmtree(frames_dir, ignore_errors=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
