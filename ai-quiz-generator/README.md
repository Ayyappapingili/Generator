# AI Quiz Generator

## Features
- Generates quiz questions using Google Gemini API
- Allows user selection of topic, difficulty, number of questions, and question type
- Flask web app with an interactive frontend

## Setup
1. Install dependencies:
pip install -r requirements.txt
2. Create `.env` file and add your API key:
GEMINI_API_KEY=your_google_gemini_api_key
3. Run the app locally:
python app.py

## Deploying on Railway
1. Push the project to GitHub.
2. Go to [Railway.app](https://railway.app/) and **deploy via GitHub**.
3. Set `GEMINI_API_KEY` in Railway **Environment Variables**.
4. Click **Deploy** and get your public URL!
