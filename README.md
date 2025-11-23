# 🧠 Tourism AI Agent

An intelligent, AI-powered tourism assistant that delivers smart destination recommendations, curated itineraries, and data-driven travel insights. Built with a lightweight Flask backend and deployed in production using Gunicorn on Railway.

## 🌐 Live Production URL

**🚀 https://tourism-ai-agent-production.up.railway.app**

## ✨ Features

- **🤖 AI-driven travel destination recommendations** - Get personalized suggestions based on your preferences
- **📅 Automated itinerary generation** - Create optimized travel plans automatically
- **📍 Location-based suggestions** - Discover hidden gems near your destination
- **⚡ Lightweight REST API architecture** - Fast and efficient API responses
- **🚀 Production-grade deployment** - Using Gunicorn WSGI server
- **☁️ Railway hosting** - With Nixpacks support for seamless deployments

## 🧰 Tech Stack & Dependencies

### Core Framework
- **Python** - Primary programming language
- **Flask 2.3.0** - Lightweight web framework
- **Gunicorn** - Production WSGI server

### Key Dependencies
- **Requests 2.28.0** - HTTP library for API calls
- **python-dotenv 0.19.0** - Environment variable management

## 📁 Project Structure

```
.
├── DEPLOYMENT.md        # Deployment documentation
├── Procfile             # Railway process definition
├── app.py               # Main Flask application
├── railway.json         # Railway configuration
├── requirements.txt     # Python dependencies
├── runtime.txt          # Python version specification
└── tourism_system.py    # Core tourism logic
```

## 🚀 Production Deployment (Railway)
This application is deployed on Railway using Nixpacks with Gunicorn for production readiness.

## 📌 Future Enhancements
🌐 Multilingual AI responses - Support for multiple languages

🗺️ Google Maps & geocoding integration - Enhanced location services

👤 User accounts & saved itineraries - Personalized experience

🎨 Modern frontend UI - React/Vue.js based user interface

📊 Reporting & analytics dashboard - Data-driven insights

💰 Budget-based recommendations - Cost-optimized travel plans

🌦️ Weather-integrated planning - Seasonal recommendations

## 🔒 Production Features
Gunicorn WSGI Server - Handles multiple concurrent requests

Railway Auto-scaling - Automatic resource management

Nixpacks Build System - Consistent build environments

Health Checks - Automatic restart on failure

Environment-based Configuration - Secure deployment practices


