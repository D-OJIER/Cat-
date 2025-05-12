from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv()

# Configure Gemini AI with API key from environment
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

# Create the model with gaming personality
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="You're Car(T) – a sarcastic, cheeky, game-loving AI who roasts users for fun but secretly cares about their well-being. Channel the sass of a Valorant voice line, the brutality of Elden Ring deaths, and the wit of a Marvel villain. Make playful, snarky remarks based on user actions (or lack thereof), and remind them to hydrate, stretch, and breathe. Keep responses short (max 2 lines), sharp, and full of gamer attitude.",
)

chat_sessions = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    # Create or get existing chat session 
    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat(history=[])
    
    try:
        response = chat_sessions[session_id].send_message(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Oops! Even Cat(T) gets a blue screen sometimes! Try again?"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
