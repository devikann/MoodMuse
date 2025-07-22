import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# 🔑 IMPORTANT: These are your Spotify credentials.
# They are sensitive and should ONLY be used on a secure backend server.
# NEVER expose them in client-side (frontend) code.
SPOTIFY_CLIENT_ID = 'YOUR SPOTIFY_CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'YOUR SPOTIFY_CLIENT_SECRET'

# Initialize Spotify client
# This block includes error handling for credential issues
try:
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    print("Spotify client initialized successfully.")
except Exception as e:
    print(f"ERROR: Failed to initialize Spotify client: {e}")
    print("Please double-check your Spotify CLIENT_ID and CLIENT_SECRET in this file.")
    sp = None # Set sp to None to prevent further errors if initialization fails

def get_spotify_songs(mood):
    """
    Fetches Spotify songs based on a given mood.
    This function is intended to be called from a backend server.
    """
    if sp is None:
        print("WARNING: Spotify client is not initialized. Cannot fetch songs.")
        return [] # Return empty list if Spotify client failed to initialize

    try:
        # --- CHANGE MADE HERE: Increased limit to 10 (you can set up to 50) ---
        # Refined search queries for better relevance
        search_query = mood # Default to just the mood
        if mood == 'happy':
            search_query = "upbeat joyful pop"
        elif mood == 'sad':
            search_query = "melancholic reflective acoustic"
        elif mood == 'energetic':
            search_query = "high energy workout electronic"
        elif mood == 'focused':
            search_query = "instrumental ambient study"
        # You can add more moods and specific queries here

        results = sp.search(q=search_query, limit=10, type='track') # Use the refined query
        songs = []
        for track in results['tracks']['items']:
            songs.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'url': track['external_urls']['spotify'],
                'preview': track['preview_url'] # Note: Preview URLs are often temporary and may not always be available
            })
        return songs
    except Exception as e:
        print(f"ERROR: Error fetching Spotify songs for mood '{mood}' with query '{search_query}': {e}")
        return []

# Example usage (for testing on a backend)
if __name__ == '__main__':
    print("\n--- Testing Spotify API Calls (Backend Only) ---")
    if sp:
        happy_songs = get_spotify_songs('happy')
        print(f"\nHappy Songs (Spotify) - {len(happy_songs)} found:")
        if happy_songs:
            for song in happy_songs:
                print(f"  - {song['name']} by {song['artist']} (Preview: {song['preview']})")
        else:
            print("  No happy songs found or an error occurred.")

        sad_songs = get_spotify_songs('sad')
        print(f"\nSad Songs (Spotify) - {len(sad_songs)} found:")
        if sad_songs:
            for song in sad_songs:
                print(f"  - {song['name']} by {song['artist']} (Preview: {song['preview']})")
        else:
            print("  No sad songs found or an error occurred.")
    else:
        print("Spotify client not initialized. Cannot test API calls. Please check credentials.")
