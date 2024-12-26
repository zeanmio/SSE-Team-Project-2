import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# -------- Routes -------- #

# Login Page
@app.route('/')
def login():
    return render_template('login.html')

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Record Dream Page
@app.route('/record')
def record_dream():
    return render_template('record.html')

# Dream Atlas Page
@app.route('/atlas')
def dream_atlas():
    return render_template('atlas.html')

# Analyze Dream Endpoint
@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    user_input = data.get("text", "")

    if not user_input:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional psychologist with expertise in dream analysis. "
                               "Provide a psychological interpretation of the following dream."
                },
                {
                    "role": "user",
                    "content": f"Analyze this dream: {user_input}"
                }
            ],
            max_tokens=500,
            temperature=0.7
        )

        # Extract and format the analysis
        analysis = response.choices[0].message.content.strip().replace("**", "").replace("\n", "<br>")
        return jsonify({"analysis": analysis})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------- Main -------- #
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
