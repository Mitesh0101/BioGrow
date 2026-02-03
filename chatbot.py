from openai import OpenAI
import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify

load_dotenv()

chatbot_bp = Blueprint("chatbot", __name__, template_folder="templates", static_folder="static")

# Initialize client once
client = OpenAI(
    api_key=os.getenv("api_key"),
    base_url="https://api.groq.com/openai/v1",
)

@chatbot_bp.route("/chatbot", methods=["POST"])
def chatbot():
    # Get the JSON Body from Request
    data = request.get_json()

    # Validate Input
    user_question = data.get("question")
    if not user_question:
        # Return the error JSON and error code 400 (Bad Request)
        return jsonify({"error": "Question cannot be empty!"}), 400
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": "You are a helpful agricultural assistant."},
                {"role": "user", "content": user_question}
            ]
        )

        bot_reply = completion.choices[0].message.content
        
        # Return clean JSON
        return jsonify({"response": bot_reply})
    
    except Exception as e:
        # Return the error JSON and error code 500
        return jsonify({"error": "Internal Server Error"}), 500