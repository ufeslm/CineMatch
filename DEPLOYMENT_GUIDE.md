# 🚀 Deployment Guide - Movie Recommendation System

## Prerequisites

1. **Get a TMDB API Key** (Required):
   - Go to https://www.themoviedb.org/
   - Create an account
   - Go to Settings > API
   - Request an API key (it's free)

2. **GitHub Account** (Required for deployment)

## 🎯 Option 1: Deploy on Render (Recommended - Easiest)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Deploy on Render
1. Go to https://render.com and sign up with GitHub
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: movie-recommendation-app
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`

### Step 3: Set Environment Variables
In Render dashboard, go to Environment tab and add:
```
SECRET_KEY=your-super-secret-key-here
TMDB_API_KEY=your-tmdb-api-key
MAIL_USERNAME=your-email@gmail.com (optional)
MAIL_PASSWORD=your-app-password (optional)
```

### Step 4: Deploy
- Click "Create Web Service"
- Wait for deployment (5-10 minutes)
- Your app will be live at: `https://your-app-name.onrender.com`

---

## 🚂 Option 2: Deploy on Railway

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy on Railway
1. Go to https://railway.app and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect it's a Python app

### Step 3: Set Environment Variables
In Railway dashboard, go to Variables tab and add:
```
SECRET_KEY=your-super-secret-key-here
TMDB_API_KEY=your-tmdb-api-key
MAIL_USERNAME=your-email@gmail.com (optional)
MAIL_PASSWORD=your-app-password (optional)
```

### Step 4: Deploy
- Railway will automatically deploy
- Your app will be live at: `https://your-app-name.up.railway.app`

---

## 🐍 Option 3: Deploy on PythonAnywhere

### Step 1: Sign up
1. Go to https://www.pythonanywhere.com
2. Create a free "Beginner" account

### Step 2: Upload Code
1. Open a Bash console
2. Clone your repository:
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### Step 3: Set up Virtual Environment
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Web App
1. Go to Web tab in dashboard
2. Click "Add a new web app"
3. Choose "Manual configuration" → Python 3.10
4. Set source code path: `/home/yourusername/your-repo-name`
5. Set working directory: `/home/yourusername/your-repo-name`

### Step 5: Configure WSGI
Edit the WSGI file to:
```python
import sys
import os

# Add your project directory to sys.path
project_home = '/home/yourusername/your-repo-name'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key'
os.environ['TMDB_API_KEY'] = 'your-tmdb-api-key'

from run import app as application
```

---

## 🔧 Environment Variables You Need

### Required:
- `SECRET_KEY`: A random secret key for Flask sessions
- `TMDB_API_KEY`: Your TMDB API key

### Optional (for email notifications):
- `MAIL_USERNAME`: Your Gmail address
- `MAIL_PASSWORD`: Your Gmail app password

---

## 🎉 After Deployment

1. **Test your app**: Visit the deployed URL
2. **Register a new account**
3. **Search for movies** and add them to favorites
4. **Get recommendations** based on your favorites

---

## 🐛 Troubleshooting

### Common Issues:

1. **App won't start**:
   - Check that `gunicorn` is in requirements.txt
   - Verify the start command is `gunicorn run:app`

2. **Database errors**:
   - The app uses SQLite by default, which works on all platforms
   - Database will be created automatically on first run

3. **API errors**:
   - Make sure your TMDB_API_KEY is set correctly
   - Test the API key at: https://api.themoviedb.org/3/movie/550?api_key=YOUR_KEY

4. **Email not working**:
   - Email is optional - the app works without it
   - If you want email, use Gmail app passwords, not your regular password

---

## 💡 Tips

1. **Free tier limitations**:
   - Render: Apps sleep after 15 minutes of inactivity
   - Railway: 500 hours/month free
   - PythonAnywhere: Always on, but limited CPU

2. **Custom domain**: Most platforms allow custom domains on paid plans

3. **Database**: For production, consider upgrading to PostgreSQL (available on all platforms)

4. **Monitoring**: Check your app's logs in the platform dashboard if issues occur

---

## 🔗 Useful Links

- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [PythonAnywhere Help](https://help.pythonanywhere.com)
- [TMDB API Documentation](https://developers.themoviedb.org/3)

---

**Need help?** Check the logs in your deployment platform's dashboard for error messages. 