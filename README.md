Tourism AI Agent

An AI-powered tourism assistant that delivers smart destination recommendations, curated itineraries, and travel-related insights.
Built with a lightweight Flask backend and deployed in production using Gunicorn on Railway.

🌐 Live Production URL
🚀 https://tourism-ai-agent-production.up.railway.app
✨ Features

AI-driven travel destination recommendations

Automated itinerary generation

Location-based suggestions

Lightweight REST API architecture

Production-grade deployment using Gunicorn

Railway hosting with Nixpacks support

🧰 Tech Stack & Dependencies

Python

Flask 2.3.0

Gunicorn (latest)

Requests 2.28.0

python-dotenv 0.19.0

📁 Project Structure
.
├── DEPLOYMENT.md
├── Procfile
├── app.py
├── railway.json
├── requirements.txt
├── runtime.txt
└── tourism_system.py

⚙️ Installation (Run Locally)
1. Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

2. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run the application
python app.py


Local development URL:

👉 http://127.0.0.1:5000

🚀 Deployment (Railway)

This application is deployed using Railway Nixpacks with Gunicorn.

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

📌 Future Enhancements

Multilingual AI responses

Google Maps & geocoding integration

User accounts & saved itineraries

Modern frontend UI

Reporting & analytics dashboard
