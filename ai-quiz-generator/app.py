import os
import json
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("⚠️ Warning: GEMINI_API_KEY not found in .env file. The API will not work.")

# Initialize Flask app with explicit static and template folders
app = Flask(__name__, static_folder="static", template_folder="templates")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Optional: Log static file requests (for debugging missing files)
@app.route('/static/<path:filename>')
def custom_static(filename):
    print(f"📁 Serving static file: {filename}")
    return send_from_directory(app.static_folder, filename)

# Function to check if API key is valid
def check_api_key():
    if not GEMINI_API_KEY:
        return {"error": "API key is missing. Please set the GEMINI_API_KEY environment variable."}
    
    test_prompt = "Say 'Hello' in a JSON response."
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {"contents": [{"parts": [{"text": test_prompt}]}]}

    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
    
    if response.status_code == 200:
        return {"success": "API key is valid."}
    else:
        return {"error": f"Invalid API key. Status Code: {response.status_code}", "details": response.text}

# Function to generate quiz
def generate_quiz(topic, difficulty, num_questions, question_type):
    if not GEMINI_API_KEY:
        return {"error": "API key is missing. Please set the GEMINI_API_KEY environment variable."}

    prompt = f"Generate {num_questions} {question_type} quiz questions on {topic} with {difficulty} difficulty. Format the output in JSON with 'question', 'options', and 'answer' fields."

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)

    if response.status_code == 200:
        try:
            result = response.json()
            print("✅ API Response:", json.dumps(result, indent=2))  # Debugging Log

            quiz_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "{}")

            if not quiz_text.strip():
                return {"error": "AI returned an empty response"}

            # Extract JSON content safely
            quiz_text = quiz_text.strip("`json\n")  # Remove JSON formatting artifacts
            quiz_json = json.loads(quiz_text)
            return {"quiz": quiz_json}
        except (json.JSONDecodeError, KeyError) as e:
            print("⚠️ JSON Parsing Error:", str(e))  # Debugging Log
            return {"error": "Invalid AI response format", "details": str(e)}
    else:
        print(f"❌ API Error {response.status_code}: {response.text}")  # Debugging Log
        return {"error": "Failed to generate quiz", "details": response.text}

# Serve Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Serve Quiz Page
@app.route("/quiz")
def quiz_page():
    return render_template("quiz.html")

# API Endpoint to Check API Key
@app.route("/check_api", methods=["GET"])
def check_api():
    return jsonify(check_api_key())

# API Endpoint to Generate Quiz
@app.route("/generate_quiz", methods=["POST"])
def generate_quiz_api():
    data = request.get_json()
    topic = data.get("topic", "General Knowledge")
    difficulty = data.get("difficulty", "Medium")
    num_questions = int(data.get("num_questions", 5))
    question_type = data.get("question_type", "multiple_choice")

    quiz = generate_quiz(topic, difficulty, num_questions, question_type)
    return jsonify(quiz)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Use Railway's provided port
    app.run(host="0.0.0.0", port=port, debug=True)  # Enable Debug Mode
