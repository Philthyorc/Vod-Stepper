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
import yt_dlp

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

    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        return jsonify({'error': 'Invalid YouTube URL format'}), 400

    video_id = match.group(1)
    normalized_url = f"https://www.youtube.com/watch?v={video_id}"

    video_path = None
    frames_dir = os.path.join("temp_frames", video_id)
    video_title = "Unknown Title"

    try:
        # Grab metadata with yt-dlp before downloading
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'cookiefile': 'youtube_cookies.txt'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(normalized_url, download=False)
            video_title = info.get("title", "Unknown Title")

        # Step 1: Download actual video
        video_path = download_video(normalized_url)

        # Step 2: Extract frames
        extract_frames(video_path, frames_dir, fps=1)

        # Step 3: Analyze frames
        report = analyze_frames(frames_dir)

        total_seconds = report["summary"]["total_seconds"]
        on_point_seconds = report["summary"]["on_point_seconds"]
        percentage = round((on_point_seconds / total_seconds) * 100, 2) if total_seconds else 0.0

        return jsonify({
            'title': video_title,
            'on_point_seconds': on_point_seconds,
            'total_seconds': total_seconds,
            'percentage': percentage
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

    finally:
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(frames_dir):
            shutil.rmtree(frames_dir, ignore_errors=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
