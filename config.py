"""
Configuration File for OAuth Credentials and Settings
Update these values with your actual OAuth credentials
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
SESSION_TYPE = 'filesystem'

# Google OAuth
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/auth/callback/google')

# Facebook OAuth
FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID', 'YOUR_FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET', 'YOUR_FACEBOOK_APP_SECRET')
FACEBOOK_REDIRECT_URI = os.getenv('FACEBOOK_REDIRECT_URI', 'http://localhost:5000/auth/callback/facebook')

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN')
TELEGRAM_BOT_USERNAME = os.getenv('TELEGRAM_BOT_USERNAME', 'YOUR_BOT_USERNAME')
TELEGRAM_REDIRECT_URI = os.getenv('TELEGRAM_REDIRECT_URI', 'http://localhost:5000/auth/callback/telegram')

# Application Settings
DEBUG = os.getenv('DEBUG', True)
HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 5000))
