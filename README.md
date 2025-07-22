🎧 MoodMuse

MoodMuse is an AI-powered web app that suggests songs from Spotify based on your mood and generates personalized music suggestions from YouTube by detecting your feelings from text prompts. It combines Flask, Gemini AI, and Spotify API to deliver a truly personalized music experience.

💡 Problem

In today’s emotionally demanding world, music remains a powerful tool for mood regulation and mental well-being. However, most platforms fail to understand and respond to users’ real-time emotions, leaving their music experiences generic and disconnected.

🚀 Solution

MoodMuse bridges this gap by:

Allowing users to select a mood (happy, sad, energetic, focused) and instantly getting recommended Spotify songs.

Analyzing user text input (e.g., “I feel exhausted after work”) using Gemini AI to detect the emotional mood and suggesting matching music via YouTube links for enhanced emotional support.

🛠️ Features

✅ Mood-based Spotify song recommendations
✅ AI-powered music suggestion from text prompts using Gemini AI
✅ Responsive web interface with Tailwind CSS
✅ Flask backend API handling Spotify and Gemini AI integration

🧰 Tech Stack

Frontend: HTML, Tailwind CSS, JavaScript

Backend: Python, Flask

APIs & Libraries: Spotipy (Spotify API), Google Gemini AI, Requests

📦 Libraries Used

Flask
Flask-Cors
spotipy
requests
transformers (for any future Hugging Face model integration)
torch (optional, if expanded to local model inference)

⚙️ Installation & Execution

🖥️ Requirements

Python 3.10+
pip (Python package manager)
Spotify Developer Account (Client ID & Secret)
Gemini AI API Key (from Google AI Studio)

🔧 Setup Instructions
1. Clone the Repository
git clone https://github.com/your-username/moodmuse.git
cd moodmuse

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate    # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Set Environment Variables
For Windows (PowerShell):
  setx SPOTIPY_CLIENT_ID "your_spotify_client_id"
  setx SPOTIPY_CLIENT_SECRET "your_spotify_client_secret"
  setx GEMINI_API_KEY "your_gemini_api_key"

5.Run the Application
python app.py

📝 Project Structure

MoodMuse/

├── app.py

├── backend/

│   ├── ai_music.py

│   └── spotify_suggestion.py

├── frontend/

│   ├── index.html

│   └── style.css

├── venv/

└── requirements.txt

✨ Future Enhancements

Integrate Magenta.js for browser-based AI music generation
Implement local generative models using Hugging Face for custom melodies
Deploy as a full-stack cloud application with user authentication
