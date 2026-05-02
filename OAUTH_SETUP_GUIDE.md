# OAuth Setup Guide for AutoMPG

This guide explains how to set up Google, Facebook, and Telegram OAuth authentication for your AutoMPG application.

## Prerequisites

- Python 3.7+
- Flask and dependencies (see requirements.txt)
- A web server accessible from the internet (for testing Telegram)

---

## 1. Google OAuth Setup

### Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google+ API

### Step 2: Create OAuth 2.0 Credentials
1. Go to **Credentials** → **Create Credentials** → **OAuth client ID**
2. Choose **Web application**
3. Add authorized redirect URIs:
   - `http://localhost:5000/auth/callback/google`
   - `https://yourdomain.com/auth/callback/google` (production)
4. Copy the **Client ID** and **Client Secret**

### Step 3: Update .env File
```
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:5000/auth/callback/google
```

---

## 2. Facebook OAuth Setup

### Step 1: Create a Facebook App
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click **My Apps** → **Create App**
3. Choose **Consumer** as the app type
4. Fill in the app details

### Step 2: Configure OAuth Redirect URIs
1. Go to **Settings** → **Basic** and copy the **App ID** and **App Secret**
2. Go to **Settings** → **Basic** and add your app domain
3. In **Facebook Login** settings, add redirect URIs:
   - `http://localhost:5000/auth/callback/facebook`
   - `https://yourdomain.com/auth/callback/facebook` (production)

### Step 3: Update .env File
```
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here
FACEBOOK_REDIRECT_URI=http://localhost:5000/auth/callback/facebook
```

---

## 3. Telegram Bot Setup

### Step 1: Create a Telegram Bot
1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow the prompts to create your bot
4. Copy the **Bot Token**

### Step 2: Configure Bot Username
1. Send `/setusername` to @BotFather
2. Choose a unique username for your bot

### Step 3: Update .env File
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_BOT_USERNAME=your_bot_username_here
TELEGRAM_REDIRECT_URI=http://localhost:5000/auth/callback/telegram
```

---

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the project root with all your OAuth credentials (see examples above).

### 3. Initialize Database
The database will be automatically initialized when you run the app for the first time.

### 4. Run the Application
```bash
python app.py
```

The app will be available at `http://localhost:5000`

---

## Key Files

- **app.py** - Main Flask application with OAuth routes
- **auth.py** - OAuth implementation for Google, Facebook, and Telegram
- **database.py** - Database operations and user management
- **config.py** - Configuration settings
- **.env** - Environment variables (create this file)
- **templates/login.html** - Login page with OAuth buttons
- **templates/index.html** - Updated main page with user profile

---

## File Structure

```
PT2/
├── app.py              # Main application
├── auth.py             # OAuth handlers
├── config.py           # Configuration
├── database.py         # Database operations
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
├── model/
│   └── train_model.py
├── templates/
│   ├── login.html      # OAuth login page
│   ├── index.html      # Main page with user profile
│   ├── compare.html
│   └── dashboard.html
├── static/
│   └── style.css
└── predictions.db      # SQLite database
```

---

## Testing OAuth Locally

For local testing, use `http://localhost:5000` as your redirect URI. Some platforms require HTTPS for production, which you can set up with:

1. **ngrok** - Tunnel localhost to HTTPS: `ngrok http 5000`
2. **Certbot** - Set up SSL certificates locally
3. **Environment-specific .env** - Use different URIs for dev/prod

---

## Database Schema

The application uses SQLite with these tables:

### users
- `id` - User ID
- `provider` - OAuth provider (google, facebook, telegram)
- `provider_id` - Provider's user ID
- `email` - User email
- `name` - User name
- `profile_picture` - Profile picture URL
- `created_at` - Timestamp

### predictions
- `id` - Prediction ID
- `user_id` - Foreign key to users
- `cylinders`, `displacement`, `horsepower`, etc. - Car features
- `predicted_mpg` - Predicted fuel efficiency
- `created_at` - Timestamp

---

## Troubleshooting

### "Invalid OAuth Credentials"
- Verify your credentials in `.env` are correct
- Check redirect URIs match exactly (including trailing slashes)
- Ensure OAuth apps are active in respective developer consoles

### "Telegram Authentication Failed"
- Verify bot token is correct
- For production, ensure your domain is HTTPS
- Test webhook configuration

### Database Errors
- Delete `predictions.db` to reset
- Re-run app.py to reinitialize

---

## Next Steps

1. Update dashboard and compare pages to show user predictions
2. Add user statistics dashboard
3. Implement social sharing features
4. Add email notifications for predictions
5. Set up rate limiting
6. Implement payment system (if needed)

---

## Support

For issues or questions:
- Check provider documentation (Google, Facebook, Telegram)
- Review OAuth 2.0 specification
- Enable debug mode in Flask: `DEBUG=True` in `.env`
