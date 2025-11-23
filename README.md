Tourism AI Agent

An intelligent, AI-powered tourism assistant that provides personalized destination recommendations, curated travel itineraries, and answers to travel-related queries.
Built with Flask, optimized for production with Gunicorn, and deployed seamlessly on Railway.

🌐 Live Production URL
🚀 https://tourism-ai-agent-production.up.railway.app
✨ Features

AI-driven travel recommendations

Automated itinerary generation

Location-based suggestions

Lightweight and simple REST API

Fast Flask backend optimized for production

Deployed using Railway + Gunicorn

🧰 Tech Stack

Python

Flask

Gunicorn

Railway (Hosting)

dotenv

requests

📁 Project Structure
.
├── app.py
├── requirements.txt
├── Procfile
├── railway.json
└── README.md

⚙️ Installation (Run Locally)
1. Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

2. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Start the application
python app.py


Local development URL:

👉 http://127.0.0.1:5000

🚀 Deployment (Railway)

This project uses Railway Nixpacks with a Gunicorn production server.

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

🔧 Environment Variables (Optional)

Create a .env file:

API_KEY=your_api_key
DEBUG=False

📡 Basic API Example
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

📌 Future Improvements

Multilingual AI responses

Google Maps API integration

User authentication & saved itineraries

Web-based frontend UI

Advanced analytics & insights
