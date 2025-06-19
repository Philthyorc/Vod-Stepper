# vod_stepper/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)  # 👈 Enables cross-origin requests from Netlify or anywhere

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

    # TODO: Replace this with your actual logic that analyzes the video
    # Dummy values for testing
    time.sleep(1)
    on_point_seconds = 157  # placeholder
    total_seconds = 340     # placeholder
    percentage = round((on_point_seconds / total_seconds) * 100, 2)

    return jsonify({
        'on_point_seconds': on_point_seconds,
        'total_seconds': total_seconds,
        'percentage': percentage
    })

if __name__ == '__main__':
    app.run(debug=True)
