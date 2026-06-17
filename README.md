# 🚀 FakeForward Detector

![FakeForward Detector Logo](https://img.shields.io/badge/Status-Deployment_Ready-success?style=for-the-badge) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![JavaScript](https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**FakeForward Detector** is an intelligent, automated fact-checking platform built to instantly analyze viral messages, WhatsApp forwards, and social media text. It extracts core claims, cross-references them against real-world evidence from the web, and grades them for factual accuracy to stop the spread of misinformation.

---

## ✨ Features

- **🧠 Intelligent Extraction:** Uses Large Language Models (LLMs) to parse messy, emoji-filled text and extract objective, checkable claims.
- **🔍 Automated Web Search:** Integrates with Wikipedia and DuckDuckGo to automatically gather real-time evidence for every extracted claim.
- **📊 Granular Grading System:** Grades each individual claim from 0-100 and assigns a clear, color-coded verdict: **TRUE**, **PROBABLE**, **FALSE**, or **UNVERIFIABLE**.
- **🎨 Immersive UI:** Features a sleek, modern chat-like interface with simulated stage progression, bouncy animations, and organic floating claim cards.
- **📱 Accessible & Responsive:** Fully responsive design built with Vanilla JavaScript and CSS, respecting `prefers-reduced-motion` settings.
- **📋 One-Click Debunking:** Easily copy the full fact-check report to your clipboard to paste right back into group chats.

---

## 🏗 Architecture

The project consists of two main components:

1. **Frontend (`/frontend`)**
   - Pure HTML, Vanilla JavaScript, and CSS.
   - Features GPU-accelerated CSS animations (aurora background, organic blob morphing).
   - Zero-dependency architecture for maximum speed and simplicity.

2. **Backend (`/backend`)**
   - **Framework:** FastAPI.
   - **Pipeline:** A multi-step asynchronous pipeline (`extractor.py` -> `searcher.py` -> `scorer.py` -> `verdict.py`).
   - **AI Integration:** Powered by LLMs (OpenAI, with support for fallback configurations).
   - **Web Scraping:** Uses `duckduckgo-search` and the Wikipedia API.

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.9+
- An OpenAI API Key (or Gemini/OpenRouter depending on your specific `.env` setup)

### 1. Clone the Repository
```bash
git clone https://github.com/aarish-ai/FakeForward-App.git
cd FakeForward-App
```

### 2. Setup the Backend
Navigate to the backend directory, create a virtual environment, and install dependencies:
```bash
cd backend
python -m venv venv

# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the `backend` directory based on the `.env.example` structure:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the Application
The backend FastAPI server is configured to automatically serve the frontend static files. Simply run:
```bash
uvicorn main:app --reload --port 8000
```
Then open your browser and navigate to: **http://localhost:8000**

---

## 🌐 Deployment
The app is fully prepared for deployment on modern PAAS platforms like Render, Heroku, or Vercel. 
- The FastAPI application automatically mounts the static `/frontend` directory to its root route.
- Absolute paths have been removed so the container executes flawlessly from the `backend/` working directory.
- Simply set your Build Command to `pip install -r requirements.txt` and your Start Command to `uvicorn main:app --host 0.0.0.0 --port 10000`.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/aarish-ai/FakeForward-App/issues).

---

*Built to combat the spread of misinformation.* 🛡️
