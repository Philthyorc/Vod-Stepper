# vod_stepper/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from pytube import YouTube
import re

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

    # Convert youtu.be short links to full YouTube format
    if "youtu.be/" in url:
        match = re.search(r"youtu\.be/([a-zA-Z0-9_-]+)", url)
        if match:
            video_id = match.group(1)
            url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        yt = YouTube(url)
        total_seconds = yt.length
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve video info: {str(e)}'}), 500

    # Placeholder logic: assume 46% point control
    on_point_seconds = int(total_seconds * 0.46)
    percentage = round((on_point_seconds / total_seconds) * 100, 2)

    return jsonify({
        'on_point_seconds': on_point_seconds,
        'total_seconds': total_seconds,
        'percentage': percentage
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
