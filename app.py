# backend/app.py (Flask Backend Server - NOW SERVES FRONTEND TOO)
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Import your helper functions
# Ensure the path is correct if spotify_suggestion.py and ai_music.py are in 'backend' subfolder
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from spotify_suggestion import get_spotify_songs
from ai_music import generate_ai_music # RE-INTRODUCED

app = Flask(__name__)
# Enable CORS for all origins. In production, consider restricting to your frontend's domain.
CORS(app)

# Define paths for static files and music files
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) # app.py is in the root now
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
MUSIC_DIR = os.path.join(BASE_DIR, 'backend', 'music') # Base music folder for Spotify previews

# Ensure music directory exists (still needed for Spotify preview MP3s if any)
if not os.path.exists(MUSIC_DIR):
    os.makedirs(MUSIC_DIR)
    print(f"Created music directory: {MUSIC_DIR}")
# No longer need to create generated_ai_music folder via backend


# --- Route to serve the main HTML file (index.html) ---
@app.route('/', methods=['GET'])
def serve_index():
    print(f"Serving index.html from: {FRONTEND_DIR}")
    return send_from_directory(FRONTEND_DIR, 'index.html')

# --- Route to serve the CSS file (style.css) ---
@app.route('/style.css', methods=['GET'])
def serve_css():
    print(f"Serving style.css from: {FRONTEND_DIR}")
    return send_from_directory(FRONTEND_DIR, 'style.css')

# Endpoint for mood-based song suggestions (e.g., Happy, Sad buttons)
@app.route('/get_songs', methods=['POST'])
def get_songs_route():
    data = request.get_json()
    mood = data.get('mood')
    if not mood:
        return jsonify({"error": "Mood not provided"}), 400

    # Call the Spotify function from your backend
    spotify_songs = get_spotify_songs(mood)
    return jsonify({"spotify_songs": spotify_songs})

# Endpoint for AI-generated music based on text prompt
@app.route('/generate_music', methods=['POST'])
def generate_music_route():
    data = request.get_json()
    text_prompt = data.get('text')
    if not text_prompt:
        return jsonify({"error": "Text prompt not provided"}), 400

    # Use your AI music logic to determine mood and get YouTube video details
    generated_result = generate_ai_music(text_prompt)

    if generated_result.get("videoId"):
        return jsonify({
            "mood": generated_result["mood"],
            "title": generated_result["title"],
            "videoId": generated_result["videoId"]
        })
    else:
        # If generate_ai_music returns an error or no videoId, propagate it
        error_message = generated_result.get("title", "Could not generate music.")
        return jsonify({"error": error_message}), 500 # Return a server error if generation failed

# Endpoint to serve static music files (MP3s) - Still needed for Spotify previews if they are local
@app.route('/music/<path:filename>')
def serve_music(filename):
    print(f"Serving music file: {filename} from {MUSIC_DIR}")
    return send_from_directory(MUSIC_DIR, filename)

if __name__ == '__main__':
    # Create dummy music files for testing if they don't exist
    dummy_mp3_content = b'\x49\x44\x33\x03\x00\x00\x00\x00\x00\x00\x54\x53\x53\x00\x00\x00\x00\x00\x00\x00'
    for f in ['happy.mp3', 'sad.mp3', 'energetic.mp3', 'focused.mp3', 'calm.mp3']: # Include calm.mp3 if you have it
        file_path = os.path.join(MUSIC_DIR, f)
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f_out:
                f_out.write(dummy_mp3_content)
            print(f"Created dummy file: {file_path}")

    print(f"\n--- Starting Combined Flask Server (Frontend & Backend) ---")
    print(f"Access the application at: http://127.0.0.1:5000")
    print(f"Ensure your Spotify CLIENT_ID and CLIENT_SECRET are updated in spotify_suggestion.py")
    print(f"AI Music Generation is now handled by backend using Gemini API (YouTube embeds).")
    app.run(debug=True, port=5000)
