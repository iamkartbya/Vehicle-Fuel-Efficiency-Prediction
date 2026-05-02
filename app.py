from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session
import pickle
import numpy as np
import os
from dotenv import load_dotenv
from datetime import timedelta
from database import init_db, save_prediction, get_history, find_or_create_user, get_user_by_id
from auth import (
    GoogleOAuth, FacebookOAuth, TelegramOAuth,
    login_required, get_current_user, logout_user
)
import config

load_dotenv()

app = Flask(__name__)

# Session Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
Session(app)

# Load model once at startup
with open("model/model.pkl", "rb") as f:
    payload = pickle.load(f)
    MODEL  = payload["model"]
    SCALER = payload["scaler"]

init_db()

@app.route("/")
def index():
    user = get_current_user()
    if user:
        history = get_history(user_id=user[0])
    else:
        history = []
    return render_template("index.html", history=history, user=user)

@app.route("/compare")
def compare():
    user = get_current_user()
    return render_template("compare.html", user=user)

@app.route("/dashboard")
def dashboard():
    user = get_current_user()
    return render_template("dashboard.html", user=user)

@app.route("/predict", methods=["POST"])
@login_required
def predict():
    try:
        user = get_current_user()
        user_id = user[0] if user else None
        
        data = request.get_json()
        features = {
            "cylinders":    float(data["cylinders"]),
            "displacement": float(data["displacement"]),
            "horsepower":   float(data["horsepower"]),
            "weight":       float(data["weight"]),
            "acceleration": float(data["acceleration"]),
            "model_year":   float(data["model_year"]),
            "origin":       float(data["origin"]),
        }
        arr = np.array([[
            features["cylinders"], features["displacement"],
            features["horsepower"], features["weight"],
            features["acceleration"], features["model_year"],
            features["origin"]
        ]])
        arr_scaled = SCALER.transform(arr)
        mpg = round(float(MODEL.predict(arr_scaled)[0]), 2)
        save_prediction(user_id, features, mpg)
        return jsonify({"success": True, "mpg": mpg})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

def validate_input(data):
    try:
        if not (3 <= float(data["cylinders"]) <= 8):
            return "Cylinders must be between 3 and 8"

        if not (50 <= float(data["horsepower"]) <= 300):
            return "Horsepower must be between 50 and 300"

        if not (1000 <= float(data["weight"]) <= 6000):
            return "Weight must be between 1000 and 6000 lbs"

        if not (5 <= float(data["acceleration"]) <= 30):
            return "Acceleration must be between 5 and 30 sec"

        if not (60 <= float(data["model_year"]) <= 90):
            return "Model year must be between 60 and 90"

        return None
    except:
        return "Invalid input format"

@app.route("/history")
@login_required
def history():
    user = get_current_user()
    rows = get_history(user_id=user[0])
    result = [
        {"id": r[0], "cylinders": r[1], "displacement": r[2], "horsepower": r[3],
         "weight": r[4], "predicted_mpg": r[5], "created_at": r[6]}
        for r in rows
    ]
    return jsonify(result)

# ──────────────────────────────────────────
# Authentication Routes
# ──────────────────────────────────────────

@app.route("/login")
def login():
    """Display login page with OAuth options"""
    return render_template("login.html",
                          google_auth_url=GoogleOAuth.get_auth_url(),
                          facebook_auth_url=FacebookOAuth.get_auth_url(),
                          telegram_login_url=TelegramOAuth.generate_login_url())

@app.route("/auth/callback/google")
def google_callback():
    """Handle Google OAuth callback"""
    code = request.args.get('code')
    if not code:
        return redirect(url_for('login'))
    
    try:
        token_data = GoogleOAuth.get_token(code)
        if not token_data or 'access_token' not in token_data:
            return redirect(url_for('login'))
        
        user_info = GoogleOAuth.get_user_info(token_data['access_token'])
        if not user_info:
            return redirect(url_for('login'))
        
        user_id = find_or_create_user(
            provider=user_info['provider'],
            provider_id=user_info['provider_id'],
            email=user_info['email'],
            name=user_info['name'],
            profile_picture=user_info['picture']
        )
        
        session['user_id'] = user_id
        session.permanent = True
        
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Google auth error: {e}")
        return redirect(url_for('login'))

@app.route("/auth/callback/facebook")
def facebook_callback():
    """Handle Facebook OAuth callback"""
    code = request.args.get('code')
    if not code:
        return redirect(url_for('login'))
    
    try:
        token_data = FacebookOAuth.get_token(code)
        if not token_data or 'access_token' not in token_data:
            return redirect(url_for('login'))
        
        user_info = FacebookOAuth.get_user_info(token_data['access_token'])
        if not user_info:
            return redirect(url_for('login'))
        
        user_id = find_or_create_user(
            provider=user_info['provider'],
            provider_id=user_info['provider_id'],
            email=user_info['email'],
            name=user_info['name'],
            profile_picture=user_info['picture']
        )
        
        session['user_id'] = user_id
        session.permanent = True
        
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Facebook auth error: {e}")
        return redirect(url_for('login'))

@app.route("/auth/callback/telegram", methods=['GET', 'POST'])
def telegram_callback():
    """Handle Telegram OAuth callback"""
    try:
        if request.method == 'POST':
            data = request.get_json()
        else:
            data = request.args.to_dict()
        
        user_info = TelegramOAuth.parse_telegram_user(data)
        if not user_info:
            return jsonify({"error": "Invalid Telegram authentication"}), 401
        
        user_id = find_or_create_user(
            provider=user_info['provider'],
            provider_id=user_info['provider_id'],
            email=user_info['email'],
            name=user_info['name'],
            profile_picture=user_info.get('picture')
        )
        
        session['user_id'] = user_id
        session.permanent = True
        
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Telegram auth error: {e}")
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for('login'))

@app.route("/user/profile")
@login_required
def user_profile():
    """Get current user profile"""
    user = get_current_user()
    if user:
        return jsonify({
            "id": user[0],
            "provider": user[1],
            "email": user[2],
            "name": user[3],
            "profile_picture": user[4]
        })
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)