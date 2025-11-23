# Deployment Guide

## Heroku Deployment

### Prerequisites
1. Heroku account (sign up at https://www.heroku.com)
2. Heroku CLI installed
3. Git initialized in your project

### Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create a Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Set Environment Variables (if needed)**
   ```bash
   heroku config:set FLASK_DEBUG=False
   ```

4. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

5. **Open Your App**
   ```bash
   heroku open
   ```

## Railway Deployment

### Prerequisites
1. Railway account (sign up at https://railway.app)
2. GitHub account (to connect your repository)
3. Git initialized in your project

### Steps

1. **Push Your Code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

2. **Create a New Project on Railway**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub account
   - Select your repository

3. **Configure Deployment**
   - Railway will automatically detect Python from `requirements.txt`
   - The start command is already configured in `Procfile`: `python app.py`
   - Railway automatically sets the `PORT` environment variable (your app already uses this)

4. **Deploy**
   - Railway will automatically start building and deploying
   - You can watch the build logs in real-time
   - Once deployed, Railway will provide a public URL (e.g., `https://your-app-name.up.railway.app`)

5. **Set Environment Variables (Optional)**
   - In Railway dashboard, go to your service → Variables
   - Add `FLASK_DEBUG=False` if you want to disable debug mode
   - The app will work without any additional environment variables

6. **Custom Domain (Optional)**
   - In Railway dashboard, go to Settings → Domains
   - Add your custom domain

### Railway-Specific Features
- ✅ Auto-detects Python from `requirements.txt`
- ✅ Uses `Procfile` for start command
- ✅ Automatically sets `PORT` environment variable
- ✅ Supports `railway.json` for advanced configuration
- ✅ Free tier available with generous limits
- ✅ Automatic HTTPS/SSL certificates

## Other Deployment Options

### Render
- Connect GitHub repository
- Select Python environment
- Set build command: `pip install -r requirements.txt`
- Set start command: `python app.py`

### PythonAnywhere
- Upload files via web interface
- Configure WSGI file to point to `app.py`
- Reload web app

## Files Ready for Deployment
- ✅ `Procfile` - Process file for Heroku/Railway
- ✅ `railway.json` - Railway-specific configuration
- ✅ `runtime.txt` - Python version specification
- ✅ `requirements.txt` - Dependencies
- ✅ `.gitignore` - Git ignore rules
- ✅ Production-ready `app.py` with environment variables

## Quick Deploy Checklist

Before deploying to Railway:
- [ ] Code is pushed to GitHub
- [ ] All dependencies are in `requirements.txt`
- [ ] `Procfile` exists with start command
- [ ] `app.py` uses `PORT` environment variable (already done)
- [ ] `.gitignore` excludes unnecessary files

