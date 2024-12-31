import os
import uuid
from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from flask_cors import CORS

# -------- Initialize Flask app -------- #

app = Flask(__name__)

# -------- Configuration -------- #

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
sqlalchemy_database_uri = os.getenv("SQLALCHEMY_DATABASE_URI")

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Initialize database
db = SQLAlchemy(app)

# -------- Models -------- #

class User(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tokens = db.relationship('Token', backref='user', lazy=True)
    dreams = db.relationship('Dream', backref='user', lazy=True)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(200), unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.uuid'), nullable=False)
    exp_dt = db.Column(db.DateTime, nullable=False)

class Dream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=True)
    upload_dt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.String(36), db.ForeignKey('user.uuid'), nullable=False)

# Create all tables if they don't exist
with app.app_context():
    db.create_all()

# -------- CORS -------- #

CORS(
    app, 
    supports_credentials=True,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:5000"], 
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
            "allow_headers": ["Content-Type"], 
            "expose_headers": ["Set-Cookie"], 
            "supports_credentials": True
        }
    }
)

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
                    "content": "You are a professional psychologist with expertise in dream analysis. Provide a psychological interpretation of the following dream."
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


# -------- User Registration and Login -------- #

@app.route('/api/user/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if the user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User exists"}), 400

    # Create new user and token
    u = User(username=username, password=password)
    db.session.add(u)
    db.session.commit()

    # Create a new token
    t = str(uuid.uuid4())
    exp = datetime.utcnow() + timedelta(days=1)
    tk = Token(token=t, user_id=u.uuid, exp_dt=exp)
    db.session.add(tk)
    db.session.commit()

    resp = make_response(jsonify({"msg": "Registered and logged in successfully"}), 200)
    resp.set_cookie('token', t, httponly=True, samesite='Lax', secure=False, max_age=86400)
    return resp

@app.route('/api/user/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Validate the user credentials
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # Delete old tokens and create a new one
    Token.query.filter_by(user_id=user.uuid).delete()
    db.session.commit()

    t = str(uuid.uuid4())
    exp = datetime.now(timezone.utc) + timedelta(days=1)
    tk = Token(token=t, user_id=user.uuid, exp_dt=exp)
    db.session.add(tk)
    db.session.commit()

    resp = make_response(jsonify({"msg": "Login success"}), 200)
    resp.set_cookie('token', t, httponly=True, samesite='Lax', secure=False, max_age=86400)
    return resp

# -------- Helper Functions -------- #

def get_current_user():
    token = request.cookies.get('token')
    if not token:
        return None
    
    tk = Token.query.filter_by(token=token).first()
    if not tk or tk.exp_dt <= datetime.now(timezone.utc):
        return None
    
    user = User.query.filter_by(uuid=tk.user_id).first()
    return user

# -------- Main -------- #
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)