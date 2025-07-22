# backend/ai_music.py

import os
import json
import requests # Used for making HTTP requests to external APIs
import random # For get_random_song

# IMPORTANT: For local development, you MUST set this environment variable
# before running app.py. Example:
# On Windows (in cmd): set GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY
# On macOS/Linux (in bash): export GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY
# Replace 'YOUR_ACTUAL_GEMINI_API_KEY' with your key from Google AI Studio.
# If this is not set, a basic keyword-based fallback will be used, and AI features will be limited.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Base URL for Gemini API
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# More diverse songs for text-based mood detection (YouTube video IDs)
TEXT_DETECTED_MOOD_SONGS = {
  "happy": [
    {"title": "Pharrell Williams - Happy", "videoId": "y6Sxv-sUYtM"},
    {"title": "Katrina & The Waves - Walking On Sunshine", "videoId": "iGxT3rbn_E0"},
    {"title": "Bruno Mars - Uptown Funk (Official Video) ft. Mark Ronson", "videoId": "OPf0RTx1p6Y"},
    {"title": "Queen - Don't Stop Me Now", "videoId": "HgzGwrmLg9M"},
  ],
  "sad": [
    {"title": "Adele - Someone Like You", "videoId": "hLQl3WcQWKQ"},
    {"title": "Billie Eilish - when the party's over", "videoId": "pbMwTqkKSFI"},
    {"title": "Coldplay - Fix You", "videoId": "k4D4vQd2c6c"},
    {"title": "Mad World - Gary Jules", "videoId": "4N3N1MlvVc4"},
  ],
  "energetic": [
    {"title": "Don't Stop Me Now - Queen", "videoId": "HgzGwrmLg9M"},
    {"title": "Eye of the Tiger - Survivor", "videoId": "QEjgX_O2EwY"},
    {"title": "Thunderstruck - AC/DC", "videoId": "v2AC41dglnM"},
    {"title": "Dua Lipa - Don't Start Now", "videoId": "U7sdC3k_w5c"},
  ],
  "focused": [
    {"title": "Lofi Hip Hop Radio - Beats to Relax/Study", "videoId": "jfKfPfyJRdk"},
    {"title": "Deep Focus - Study Music", "videoId": "Wj1qJ4dMhgs"},
    {"title": "Weightless - Marconi Union", "videoId": "UfcAVejslrU"},
    {"title": "Ambient Study Music - Concentration", "videoId": "x_eI2-790qQ"},
  ],
  "calm": [
    {"title": "Weightless - Marconi Union", "videoId": "UfcAVejslrU"},
    {"title": "Enya - Orinoco Flow", "videoId": "Lg7o8I5B0q8"},
    {"title": "Relaxing Music for Stress Relief", "videoId": "S_vJ0q0_1_Y"},
    {"title": "Peaceful Piano Music", "videoId": "O9-D7Kj6C2U"},
  ],
  "neutral": [ # Default for less specific moods or if detection fails
    {"title": "Background Music for Videos", "videoId": "N3b-Q_yYg2Y"},
    {"title": "Chillhop Music", "videoId": "5qap5aO4i9A"},
    {"title": "Relaxing Jazz Music", "videoId": "H_a4O2k-x7A"},
  ],
}

def get_random_song(songs):
    """Utility to get a random song from a list."""
    if not songs:
        return None
    return random.choice(songs)

def generate_ai_music(text_prompt):
    """
    Uses the Gemini API to detect mood from text and suggest a YouTube video.
    This simulates AI music generation by providing a relevant track.
    """
    if not GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY is NOT set. AI music generation will use a simple keyword fallback.")
        # Fallback to a simple keyword detection if API key is missing
        text_prompt_lower = text_prompt.lower()
        mood = "neutral" # Default fallback mood
        if "happy" in text_prompt_lower or "good day" in text_prompt_lower or "feeling good" in text_prompt_lower:
            mood = "happy"
        elif "sad" in text_prompt_lower or "rough day" in text_prompt_lower or "down" in text_prompt_lower:
            mood = "sad"
        elif "energetic" in text_prompt_lower or "energy" in text_prompt_lower:
            mood = "energetic"
        elif "focused" in text_prompt_lower or "focus" in text_prompt_lower or "study" in text_prompt_lower:
            mood = "focused"
        elif "calm" in text_prompt_lower or "relax" in text_prompt_lower or "chill" in text_prompt_lower:
            mood = "calm"

        selected_song = get_random_song(TEXT_DETECTED_MOOD_SONGS.get(mood, TEXT_DETECTED_MOOD_SONGS["neutral"]))
        if selected_song:
            print(f"DEBUG: Using keyword fallback. Detected mood: {mood}, Selected song: {selected_song['title']}")
            return {"mood": mood, "title": selected_song["title"], "videoId": selected_song["videoId"]}
        print("ERROR: Keyword fallback also failed to select a song.")
        return {"mood": "neutral", "title": "No AI music generated (API key missing/fallback failed)", "videoId": ""}


    prompt = f"""Analyze the following text for the user's mood and suggest a suitable music vibe.
    The mood should be ONE of: "happy", "sad", "energetic", "focused", "calm", or "neutral".
    The musicVibe should be a short description of the type of music.
    Return the response in JSON format: {{"mood": "...", "musicVibe": "..."}}.

    Text: "{text_prompt}"
    """

    headers = {
        'Content-Type': 'application/json',
    }
    params = {
        'key': GEMINI_API_KEY,
    }
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "mood": {"type": "STRING"},
                    "musicVibe": {"type": "STRING"}
                },
                "propertyOrdering": ["mood", "musicVibe"]
            }
        }
    }

    try:
        print(f"DEBUG: Attempting Gemini API call with URL: {GEMINI_API_URL} and params: {params}")
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()
        print(f"DEBUG: Raw Gemini API response: {json.dumps(result, indent=2)}")

        if result.get("candidates") and result["candidates"][0].get("content") and \
           result["candidates"][0]["content"].get("parts"):
            json_string = result["candidates"][0]["content"]["parts"][0]["text"]
            print(f"DEBUG: Gemini API extracted JSON string: {json_string}")
            
            # The API might sometimes return non-JSON or partial JSON if it fails to adhere to schema
            try:
                parsed_json = json.loads(json_string)
            except json.JSONDecodeError:
                print(f"ERROR: Failed to parse JSON from Gemini API response. Raw text: {json_string}")
                return {"mood": "neutral", "title": "AI generation failed (JSON parse error in response)", "videoId": ""}

            detected_mood = parsed_json.get("mood", "neutral").lower()
            print(f"DEBUG: Detected mood from AI: {detected_mood}")

            selected_song = get_random_song(TEXT_DETECTED_MOOD_SONGS.get(detected_mood, TEXT_DETECTED_MOOD_SONGS["neutral"]))

            if selected_song:
                print(f"DEBUG: Selected song for mood {detected_mood}: {selected_song['title']}")
                return {"mood": detected_mood, "title": selected_song["title"], "videoId": selected_song["videoId"]}
            else:
                print(f"WARNING: No song found for detected mood: {detected_mood}. Falling back to neutral.")
                fallback_song = get_random_song(TEXT_DETECTED_MOOD_SONGS["neutral"])
                return {"mood": detected_mood, "title": fallback_song["title"], "videoId": fallback_song["videoId"]}

        else:
            print("ERROR: Gemini API response structure unexpected. Missing candidates/content/parts.")
            print(f"Full response: {json.dumps(result, indent=2)}")
            return {"mood": "neutral", "title": "AI generation failed (unexpected response)", "videoId": ""}

    except requests.exceptions.RequestException as e:
        print(f"ERROR: HTTP Request failed to Gemini API: {e}")
        if response is not None:
            print(f"HTTP Status Code: {response.status_code}")
            print(f"HTTP Response Text: {response.text}")
        return {"mood": "neutral", "title": f"AI generation failed (API error: {e})", "videoId": ""}
    except Exception as e:
        print(f"ERROR: An unexpected error occurred during AI music generation: {e}")
        return {"mood": "neutral", "title": "AI generation failed (unknown error)", "videoId": ""}

# Example usage (for testing on a backend)
if __name__ == '__main__':
    print("--- Testing AI Music Generation (Backend Only) ---")
    # For local testing, you can uncomment and set your GEMINI_API_KEY here
    # os.environ["GEMINI_API_KEY"] = "YOUR_ACTUAL_GEMINI_API_KEY_FOR_TESTING"
    
    result_happy = generate_ai_music("I'm feeling fantastic today, full of joy!")
    print("\nPrompt: 'I'm feeling fantastic today, full of joy!'")
    print(f"Generated Music Result: {result_happy}")

    result_sad = generate_ai_music("Had a really tough day, feeling down.")
    print("\nPrompt: 'Had a really tough day, feeling down.'")
    print(f"Generated Music Result: {result_sad}")
