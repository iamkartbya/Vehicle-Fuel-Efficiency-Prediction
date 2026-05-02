"""
OAuth and Authentication Module
Handles Google, Facebook, and Telegram login
"""
import requests
import json
from functools import wraps
from flask import session, redirect, url_for, current_app, jsonify
from database import find_or_create_user, get_user_by_id

# OAuth Configuration
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"
GOOGLE_REDIRECT_URI = "http://localhost:5000/auth/callback/google"

FACEBOOK_APP_ID = "YOUR_FACEBOOK_APP_ID"
FACEBOOK_APP_SECRET = "YOUR_FACEBOOK_APP_SECRET"
FACEBOOK_REDIRECT_URI = "http://localhost:5000/auth/callback/facebook"

TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_REDIRECT_URI = "http://localhost:5000/auth/callback/telegram"

# Google OAuth
class GoogleOAuth:
    AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://www.googleapis.com/oauth2/v4/token"
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"
    
    @staticmethod
    def get_auth_url():
        """Generate Google OAuth authorization URL"""
        return (
            f"{GoogleOAuth.AUTHORIZATION_BASE_URL}?"
            f"client_id={GOOGLE_CLIENT_ID}&"
            f"redirect_uri={GOOGLE_REDIRECT_URI}&"
            f"response_type=code&"
            f"scope=openid%20profile%20email&"
            f"access_type=offline"
        )
    
    @staticmethod
    def get_token(code):
        """Exchange authorization code for access token"""
        data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        response = requests.post(GoogleOAuth.TOKEN_URL, data=data)
        return response.json() if response.status_code == 200 else None
    
    @staticmethod
    def get_user_info(access_token):
        """Get user info from Google"""
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(GoogleOAuth.USER_INFO_URL, headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                "provider": "google",
                "provider_id": user_data.get("id"),
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "picture": user_data.get("picture")
            }
        return None


# Facebook OAuth
class FacebookOAuth:
    AUTHORIZATION_BASE_URL = "https://www.facebook.com/v12.0/dialog/oauth"
    TOKEN_URL = "https://graph.facebook.com/v12.0/oauth/access_token"
    USER_INFO_URL = "https://graph.facebook.com/me"
    
    @staticmethod
    def get_auth_url():
        """Generate Facebook OAuth authorization URL"""
        return (
            f"{FacebookOAuth.AUTHORIZATION_BASE_URL}?"
            f"client_id={FACEBOOK_APP_ID}&"
            f"redirect_uri={FACEBOOK_REDIRECT_URI}&"
            f"scope=email,public_profile&"
            f"response_type=code"
        )
    
    @staticmethod
    def get_token(code):
        """Exchange authorization code for access token"""
        data = {
            "client_id": FACEBOOK_APP_ID,
            "client_secret": FACEBOOK_APP_SECRET,
            "code": code,
            "redirect_uri": FACEBOOK_REDIRECT_URI
        }
        response = requests.get(FacebookOAuth.TOKEN_URL, params=data)
        return response.json() if response.status_code == 200 else None
    
    @staticmethod
    def get_user_info(access_token):
        """Get user info from Facebook"""
        params = {
            "access_token": access_token,
            "fields": "id,name,email,picture.type(large)"
        }
        response = requests.get(FacebookOAuth.USER_INFO_URL, params=params)
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                "provider": "facebook",
                "provider_id": user_data.get("id"),
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "picture": user_data.get("picture", {}).get("data", {}).get("url")
            }
        return None


# Telegram OAuth (using URL hash verification)
class TelegramOAuth:
    @staticmethod
    def generate_login_url():
        """Generate Telegram login button URL"""
        return f"https://oauth.telegram.org/login?bot_id=YOUR_BOT_ID&origin=http://localhost:5000&return_to=http://localhost:5000/auth/callback/telegram"
    
    @staticmethod
    def verify_telegram_auth(data):
        """Verify Telegram authentication data"""
        import hmac
        import hashlib
        
        check_hash = data.get('hash')
        if not check_hash:
            return False
        
        # Create data string for verification
        data_check_arr = []
        for key in sorted(data.keys()):
            if key != 'hash':
                data_check_arr.append(f"{key}={data[key]}")
        
        data_check_string = "\n".join(data_check_arr)
        
        # Verify hash
        secret_key = hashlib.sha256(TELEGRAM_BOT_TOKEN.encode()).digest()
        computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        
        return computed_hash == check_hash
    
    @staticmethod
    def parse_telegram_user(data):
        """Parse Telegram user data"""
        if TelegramOAuth.verify_telegram_auth(data):
            return {
                "provider": "telegram",
                "provider_id": data.get("id"),
                "email": f"tg_{data.get('id')}@telegram.local",
                "name": f"{data.get('first_name', '')} {data.get('last_name', '')}".strip(),
                "picture": data.get("photo_url")
            }
        return None


# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Get current user
def get_current_user():
    """Get the currently logged-in user"""
    if 'user_id' in session:
        user = get_user_by_id(session['user_id'])
        return user
    return None


# Logout
def logout_user():
    """Logout the current user"""
    session.clear()
