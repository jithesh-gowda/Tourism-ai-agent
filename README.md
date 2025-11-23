README.md
Tourism AI Agent

An AI-powered tourism assistant that provides destination recommendations, travel itineraries, and answers travel-related questions.
This project uses Flask, runs in production with Gunicorn, and is deployed on Railway.

Features

AI-powered travel recommendations

Itinerary generation

Location-based suggestions

Simple API structure

Fast and lightweight Flask backend

Production deployment using Gunicorn + Railway

Tech Stack

Python

Flask

Gunicorn

Railway (Hosting)

dotenv, requests

Project Structure
.
├── app.py
├── requirements.txt
├── Procfile
├── railway.json
└── README.md

Installation (Run Locally)
1. Clone the project
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run the application
python app.py


Local URL:

http://127.0.0.1:5000

Deployment (Railway)

This project is deployed on Railway using Nixpacks and Gunicorn.

Procfile
web: gunicorn app:app --bind 0.0.0.0:${PORT}

railway.json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:${PORT}",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}

Live URL (Production)

Your app is live at:

https://tourism-ai-agent-production.up.railway.app

Environment Variables (Optional)

Create a .env file for keys:

API_KEY=your_api_key
DEBUG=False

Basic API Example
Request
POST /recommend
{
  "query": "Best places to visit in Karnataka"
}

Response
{
  "results": [
    "Coorg",
    "Chikmagalur",
    "Jog Falls"
  ]
}

Future Improvements

Multilingual AI responses

Google Maps integration

User accounts & saved itineraries

Frontend UI

Advanced analytics
