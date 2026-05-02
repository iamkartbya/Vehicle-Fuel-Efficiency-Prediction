from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session
import pickle
import numpy as np
import os
from dotenv import load_dotenv
from datetime import timedelta
from database import init_db, save_prediction, get_history
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
    history = get_history()
    return render_template("index.html", history=history)

@app.route("/compare")
def compare():
    return render_template("compare.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
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
        save_prediction(None, features, mpg)
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
def history():
    rows = get_history()
    result = [
        {"id": r[0], "cylinders": r[1], "displacement": r[2], "horsepower": r[3],
         "weight": r[4], "predicted_mpg": r[5], "created_at": r[6]}
        for r in rows
    ]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)