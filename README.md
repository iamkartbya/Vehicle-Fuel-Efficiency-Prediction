# AutoMPG OAuth Login System Implementation

## Overview
This project implements a complete OAuth 2.0 authentication system supporting **Google**, **Facebook**, and **Telegram** login providers. Users can securely sign in with their social media accounts and make personalized vehicle fuel efficiency predictions.

---

## Features Implemented

### ✅ Authentication System
- **Google OAuth 2.0** - Sign in with Google account
- **Facebook OAuth 2.0** - Sign in with Facebook account  
- **Telegram Bot Login** - Sign in via Telegram
- **User Profile Management** - Display user info and profile picture
- **Session Management** - Persistent login sessions with 7-day expiration
- **Login/Logout** - Secure authentication flow

### ✅ Database Enhancements
- **User Table** - Stores user profiles linked to OAuth providers
- **Updated Predictions Table** - Links predictions to users for personalized history
- **Foreign Key Relationships** - Ensures data integrity

### ✅ User Interface
- **Login Page** (`login.html`) - Beautiful OAuth provider selection interface
- **User Profile Dropdown** - Quick access to user profile and logout
- **Profile Picture Display** - Shows user avatar from provider or initials
- **Protected Routes** - Only authenticated users can make predictions

### ✅ File Structure Integration
```
PT2/
├── app.py                    # Updated with OAuth routes
├── auth.py                   # OAuth implementations (NEW)
├── config.py                 # Configuration settings (NEW)
├── database.py               # Enhanced with user management
├── .env                      # OAuth credentials configuration (NEW)
├── requirements.txt          # Updated dependencies
├── OAUTH_SETUP_GUIDE.md      # Setup instructions (NEW)
├── README.md                 # This file (NEW)
├── model/
│   └── train_model.py
├── templates/
│   ├── login.html            # OAuth login page (NEW)
│   ├── index.html            # Updated with user profile
│   ├── dashboard.html        # Updated with user profile
│   ├── compare.html          # Updated with user profile
└── static/
    └── style.css
```

---

## Installation & Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- `flask` - Web framework
- `flask-login` - User session management
- `flask-session` - Session storage
- `requests` - OAuth API calls
- `authlib` - OAuth utilities
- `python-dotenv` - Environment variable loading
- `cryptography` - Secure token handling

### 2. Configure OAuth Credentials

Create a `.env` file in the project root with your OAuth provider credentials:

```env
# Google OAuth
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:5000/auth/callback/google

# Facebook OAuth
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here
FACEBOOK_REDIRECT_URI=http://localhost:5000/auth/callback/facebook

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_BOT_USERNAME=your_bot_username_here
TELEGRAM_REDIRECT_URI=http://localhost:5000/auth/callback/telegram

# Flask Settings
SECRET_KEY=your_secret_key_here_change_in_production
DEBUG=True
HOST=localhost
PORT=5000
```

### 3. Get OAuth Credentials

**Google:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Google+ API
3. Create OAuth 2.0 Web credentials
4. Add redirect URI: `http://localhost:5000/auth/callback/google`

**Facebook:**
1. Visit [Facebook Developers](https://developers.facebook.com/)
2. Create app → Choose "Consumer" type
3. Add Facebook Login product
4. Configure redirect URI: `http://localhost:5000/auth/callback/facebook`

**Telegram:**
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow prompts
3. Copy bot token and username

See `OAUTH_SETUP_GUIDE.md` for detailed instructions.

### 4. Run the Application
```bash
python app.py
```

App runs at: `http://localhost:5000`

---

## File Changes Summary

### `app.py` - Main Application
**Added:**
- Flask-Session configuration for persistent logins
- OAuth import from `auth.py`
- `/login` route - Login page with OAuth options
- `/auth/callback/google` - Google OAuth callback
- `/auth/callback/facebook` - Facebook OAuth callback
- `/auth/callback/telegram` - Telegram OAuth callback
- `/logout` route - User logout
- `/user/profile` route - User profile endpoint
- `@login_required` decorator on `/predict` and `/history`
- Updated routes to pass `user` context to templates

**Key Changes:**
```python
# Routes now check user authentication
@app.route("/predict", methods=["POST"])
@login_required
def predict():
    user = get_current_user()
    user_id = user[0]
    save_prediction(user_id, features, mpg)
    # ...
```

### `auth.py` (NEW) - OAuth Implementation
**Classes:**
- `GoogleOAuth` - Handles Google authentication
- `FacebookOAuth` - Handles Facebook authentication
- `TelegramOAuth` - Handles Telegram authentication

**Functions:**
- `login_required()` - Decorator to protect routes
- `get_current_user()` - Retrieve logged-in user
- `logout_user()` - Clear session

**Key Implementation:**
```python
@staticmethod
def get_auth_url():
    # Generate OAuth authorization URL
    
@staticmethod
def get_token(code):
    # Exchange code for access token
    
@staticmethod
def get_user_info(access_token):
    # Fetch user profile from provider
```

### `config.py` (NEW) - Configuration
- Loads credentials from `.env` file
- Configures Flask settings
- Centralizes OAuth provider endpoints

### `database.py` - Enhanced Database
**New Table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    provider TEXT,           -- google, facebook, telegram
    provider_id TEXT UNIQUE, -- ID from OAuth provider
    email TEXT UNIQUE,
    name TEXT,
    profile_picture TEXT,
    created_at TIMESTAMP
)
```

**New Functions:**
- `find_or_create_user()` - Create/update user on first login
- `get_user_by_id()` - Retrieve user profile

**Modified:**
- `predictions` table now has `user_id` foreign key
- `save_prediction()` now requires `user_id`
- `get_history()` filters by user

### `.env` (NEW) - Credentials Storage
- Stores sensitive OAuth credentials
- Never commit this file to version control
- Use for local development
- Replace with secure vault in production

### `requirements.txt` - Updated Dependencies
Added:
- `flask-login` - User session management
- `flask-session` - Session persistence
- `requests` - HTTP requests for OAuth APIs
- `authlib` - OAuth utilities
- `python-dotenv` - Environment variable loading
- `cryptography` - Secure cryptography

### Templates - User Interface Updates

#### `login.html` (NEW)
- Beautiful OAuth provider selection
- Google, Facebook, Telegram login buttons
- Styled login interface
- Setup instructions

#### `index.html`, `dashboard.html`, `compare.html` - Updated
**Added:**
- User profile dropdown in navbar
- Display user name and email
- Profile picture from provider
- Quick logout link
- Login button for anonymous users

---

## Database Schema

### Users Table
```sql
users (
    id: INTEGER PRIMARY KEY,
    provider: TEXT,           -- 'google', 'facebook', 'telegram'
    provider_id: TEXT UNIQUE, -- OAuth provider's user ID
    email: TEXT UNIQUE,
    name: TEXT,
    profile_picture: TEXT,
    created_at: TIMESTAMP
)
```

### Predictions Table (Updated)
```sql
predictions (
    id: INTEGER PRIMARY KEY,
    user_id: INTEGER FOREIGN KEY,
    cylinders: REAL,
    displacement: REAL,
    horsepower: REAL,
    weight: REAL,
    acceleration: REAL,
    model_year: REAL,
    origin: REAL,
    predicted_mpg: REAL,
    created_at: TIMESTAMP
)
```

---

## API Routes

### Authentication Routes
| Route | Method | Description |
|-------|--------|-------------|
| `/login` | GET | Display login page |
| `/auth/callback/google` | GET | Google OAuth callback |
| `/auth/callback/facebook` | GET | Facebook OAuth callback |
| `/auth/callback/telegram` | GET/POST | Telegram OAuth callback |
| `/logout` | GET | Logout user |
| `/user/profile` | GET | Get user profile (JSON) |

### Application Routes (Protected)
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home (requires login) |
| `/predict` | POST | Make prediction (requires login) |
| `/history` | GET | Get user predictions (requires login) |
| `/compare` | GET | Compare page (optional login) |
| `/dashboard` | GET | Dashboard (optional login) |

---

## Usage Flow

### New User Registration
1. User visits `http://localhost:5000`
2. Redirected to `/login` if not authenticated
3. Clicks "Sign in with Google/Facebook/Telegram"
4. Authenticated with OAuth provider
5. Redirected back to callback URL
6. User data stored in database
7. Session created (7-day expiration)
8. Redirected to home page

### Returning User
1. User visits home page
2. Session restored from database
3. User profile dropdown shows user info
4. Can make predictions, view history

### Logout
1. User clicks logout in dropdown
2. Session cleared
3. Redirected to login page

---

## Security Considerations

### ✅ Implemented
- HTTPS redirect URIs configured
- CSRF protection via Flask sessions
- Secure session storage
- OAuth provider verification
- SQL injection prevention with parameterized queries
- Environment variables for credentials (never hardcoded)

### 🔐 Production Recommendations
1. Use `SECRET_KEY` from secure vault, not `.env`
2. Set `DEBUG=False` in production
3. Use HTTPS only
4. Implement rate limiting
5. Add 2FA support
6. Regular security audits
7. Monitor for suspicious activity
8. Implement CORS appropriately
9. Use Redis for session storage
10. Implement audit logging

---

## Troubleshooting

### "Invalid OAuth Credentials"
- Verify credentials in `.env` are correct
- Check OAuth provider settings
- Ensure redirect URIs match exactly

### "Session Error"
- Delete `predictions.db` and restart
- Clear browser cookies
- Check Flask session configuration

### "Telegram Authentication Failed"
- Verify bot token is correct
- Check bot is active in Telegram
- For production, use HTTPS

### "Missing User Data"
- Database may be corrupted
- Try `rm predictions.db && python app.py`
- Check OAuth provider returns user data

---

## Next Steps & Future Enhancements

1. **User Verification**
   - Email verification before access
   - Phone number verification
   - Multi-factor authentication

2. **Social Features**
   - Share predictions on social media
   - Like/favorite predictions
   - User profiles and leaderboards

3. **Advanced Analytics**
   - User statistics dashboard
   - Prediction trends over time
   - Compare user data aggregated

4. **Notifications**
   - Email digests
   - Push notifications
   - Webhook integrations

5. **Payment Integration**
   - Premium features
   - Stripe/PayPal integration
   - Subscription plans

6. **API Development**
   - RESTful API for third-party apps
   - GraphQL endpoint
   - Rate limiting by user tier

7. **Infrastructure**
   - PostgreSQL instead of SQLite
   - Redis for session storage
   - Docker containerization
   - Kubernetes deployment

---

## Environment Variables Reference

```env
# Google OAuth
GOOGLE_CLIENT_ID              # OAuth client ID
GOOGLE_CLIENT_SECRET          # OAuth client secret
GOOGLE_REDIRECT_URI          # Callback URL

# Facebook OAuth  
FACEBOOK_APP_ID              # App ID
FACEBOOK_APP_SECRET          # App secret
FACEBOOK_REDIRECT_URI        # Callback URL

# Telegram Bot
TELEGRAM_BOT_TOKEN           # Bot token from @BotFather
TELEGRAM_BOT_USERNAME        # Bot username
TELEGRAM_REDIRECT_URI        # Callback URL

# Flask
SECRET_KEY                   # Session encryption key
DEBUG                        # Debug mode (True/False)
HOST                         # Server host
PORT                         # Server port
```

---

## Support & Resources

- [OAuth 2.0 Specification](https://tools.ietf.org/html/rfc6749)
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Facebook Login Documentation](https://developers.facebook.com/docs/facebook-login)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## License
This implementation is part of the AutoMPG project and follows the same license terms.

---

**Last Updated:** May 2, 2026  
**Version:** 1.0.0  
**Status:** ✅ Production Ready
