import sqlite3
from datetime import datetime

DB_PATH = "predictions.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            provider        TEXT,
            provider_id     TEXT,
            email           TEXT UNIQUE,
            name            TEXT,
            profile_picture TEXT,
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Predictions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            cylinders   REAL,
            displacement REAL,
            horsepower  REAL,
            weight      REAL,
            acceleration REAL,
            model_year  REAL,
            origin      REAL,
            predicted_mpg REAL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

# User functions
def find_or_create_user(provider, provider_id, email, name, profile_picture=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check if user exists
    c.execute('SELECT id FROM users WHERE provider = ? AND provider_id = ?', (provider, provider_id))
    user = c.fetchone()
    
    if user:
        user_id = user[0]
        # Update user info
        c.execute('''UPDATE users SET email = ?, name = ?, profile_picture = ? 
                     WHERE id = ?''', (email, name, profile_picture, user_id))
    else:
        # Create new user
        c.execute('''INSERT INTO users (provider, provider_id, email, name, profile_picture)
                     VALUES (?, ?, ?, ?, ?)''', 
                  (provider, provider_id, email, name, profile_picture))
        user_id = c.lastrowid
    
    conn.commit()
    conn.close()
    return user_id

def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, provider, email, name, profile_picture FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user


def save_prediction(user_id, features: dict, mpg: float):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO predictions
        (user_id, cylinders, displacement, horsepower, weight, acceleration, model_year, origin, predicted_mpg)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, features["cylinders"], features["displacement"], features["horsepower"],
        features["weight"], features["acceleration"], features["model_year"],
        features["origin"], mpg
    ))
    conn.commit()
    conn.close()

def get_history(user_id=None, limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if user_id:
        c.execute('''
            SELECT id, cylinders, displacement, horsepower, weight, predicted_mpg, created_at
            FROM predictions WHERE user_id = ? ORDER BY created_at DESC LIMIT ?
        ''', (user_id, limit))
    else:
        c.execute('''
            SELECT id, cylinders, displacement, horsepower, weight, predicted_mpg, created_at
            FROM predictions ORDER BY created_at DESC LIMIT ?
        ''', (limit,))
    
    rows = c.fetchall()
    conn.close()
    return rows