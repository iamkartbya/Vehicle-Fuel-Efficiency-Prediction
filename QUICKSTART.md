# Quick Start Guide - AutoMPG OAuth Implementation

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create OAuth Apps (2 minutes per service)

**Google:**
1. Go to https://console.cloud.google.com/
2. Create new project → APIs → Google+ API → Enable
3. Credentials → OAuth 2.0 Client ID (Web)
4. Authorized redirect: `http://localhost:5000/auth/callback/google`
5. Copy Client ID & Secret

**Facebook:**
1. Go to https://developers.facebook.com/
2. My Apps → Create App → Consumer
3. Settings → Basic → Copy App ID & Secret
4. Add redirect: `http://localhost:5000/auth/callback/facebook`

**Telegram:**
1. Message @BotFather on Telegram
2. `/newbot` → Name your bot → Get bot token
3. `/setusername` → Set username
4. Copy bot token and username

### Step 3: Configure .env File
```bash
cp .env.example .env  # or create manually
```

Edit `.env` with your credentials:
```env
GOOGLE_CLIENT_ID=your_id
GOOGLE_CLIENT_SECRET=your_secret
GOOGLE_REDIRECT_URI=http://localhost:5000/auth/callback/google

FACEBOOK_APP_ID=your_id
FACEBOOK_APP_SECRET=your_secret
FACEBOOK_REDIRECT_URI=http://localhost:5000/auth/callback/facebook

TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_BOT_USERNAME=your_username
TELEGRAM_REDIRECT_URI=http://localhost:5000/auth/callback/telegram

SECRET_KEY=any-random-string-here
DEBUG=True
```

### Step 4: Run Application
```bash
python app.py
```

Application runs at: **http://localhost:5000**

---

## 📋 What's Been Implemented

✅ **Google OAuth 2.0 Login**
✅ **Facebook OAuth 2.0 Login**  
✅ **Telegram Bot Login**
✅ **User Profile Management**
✅ **User-Specific Predictions**
✅ **Session Management** (7-day expiration)
✅ **Beautiful Login Page**
✅ **User Profile Dropdown**
✅ **Protected Routes** (login required)
✅ **Database with User Storage**

---

## 🎯 Key Features

### Login Page
- Beautiful OAuth provider buttons
- Multiple login options
- Responsive design

### User Profile
- Shows user name & email
- Profile picture from provider
- Quick logout link
- Profile view endpoint

### Database
- Users table with OAuth provider info
- User-specific prediction history
- Secure credential storage

### API Routes
```
GET  /login                    → Login page
GET  /auth/callback/google     → Google OAuth callback
GET  /auth/callback/facebook   → Facebook OAuth callback
GET  /auth/callback/telegram   → Telegram OAuth callback
GET  /logout                   → Logout
GET  /user/profile             → User profile (JSON)
POST /predict                  → Make prediction (protected)
GET  /history                  → User history (protected)
```

---

## 📁 Project Structure

```
PT2/
├── app.py                      # Flask app with OAuth routes
├── auth.py                     # OAuth implementations
├── config.py                   # Configuration
├── database.py                 # Database operations
├── requirements.txt            # Python dependencies
├── .env                        # OAuth credentials
├── OAUTH_SETUP_GUIDE.md        # Detailed setup
├── README.md                   # Full documentation
├── QUICKSTART.md               # This file
├── templates/
│   ├── login.html              # Login page (NEW)
│   ├── index.html              # Home with user profile
│   ├── dashboard.html          # Dashboard
│   └── compare.html            # Compare tool
└── model/
    └── train_model.py
```

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'flask_session'"
```bash
pip install flask-session
```

### "OAuth request failed"
- Check credentials in `.env` are correct
- Verify redirect URIs match exactly
- Ensure OAuth apps are active

### "Database error"
```bash
rm predictions.db
python app.py  # Reinitialize
```

### "Invalid credentials error"
- Are you using correct Client ID/Secret?
- Did you enable the OAuth API?
- Is redirect URI configured?

---

## 🌐 Testing OAuth Locally

### Local Testing
- Use `http://localhost:5000` in OAuth settings
- Works for Google and Facebook
- Telegram requires HTTPS (use ngrok)

### Using ngrok for HTTPS Tunnel
```bash
ngrok http 5000
# Get HTTPS URL: https://xxxxx.ngrok.io
# Update OAuth redirect URIs with this URL
```

---

## 📊 Database Schema

**Users Table**
- id, provider, provider_id, email, name, profile_picture, created_at

**Predictions Table** (updated)
- id, user_id, cylinders, displacement, horsepower, weight, acceleration, model_year, origin, predicted_mpg, created_at

---

## 🔐 Security Notes

✅ Environment variables for credentials (never hardcoded)
✅ CSRF protection via Flask sessions
✅ OAuth provider verification
✅ SQL injection prevention
✅ Secure session storage

⚠️ For production:
- Use HTTPS only
- Set DEBUG=False
- Use secure SECRET_KEY
- Implement rate limiting
- Monitor OAuth logs
- Use production database

---

## 📝 Next Steps

1. ✅ Get OAuth credentials from providers
2. ✅ Create `.env` file with credentials
3. ✅ Run application
4. ✅ Test OAuth login
5. ⏭️ Make predictions
6. ⏭️ Deploy to production

---

## 💡 Tips

- **First time?** Read OAUTH_SETUP_GUIDE.md for detailed steps
- **Need help?** Check README.md for full documentation
- **Want to deploy?** Use Docker or cloud platform
- **Privacy concern?** All credentials stored locally in .env

---

## 📞 Support

For issues:
1. Check if credentials are correct in `.env`
2. Verify OAuth provider settings
3. Check browser console for errors
4. Review Flask debug output
5. See README.md troubleshooting section

---

**Ready to use!** 🎉
