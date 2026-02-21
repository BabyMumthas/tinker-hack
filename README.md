<p align="center">
  <h1 align="center">🔍 Missing Person AI — National Missing Person Support System</h1>
  <p align="center">
    <em>AI-powered facial recognition platform for reporting, tracking, and recovering missing persons</em>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/DeepFace-ArcFace-orange?logo=tensorflow&logoColor=white" />
  <img src="https://img.shields.io/badge/Gemini_AI-Chatbot-4285F4?logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/Twilio-WhatsApp-25D366?logo=whatsapp&logoColor=white" />
</p>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Environment Variables](#-environment-variables)
- [Usage](#-usage)
- [Deployment](#-deployment)
- [Future Enhancements](#-future-enhancements)

---

## Overview

**Missing Person AI** is a full-stack web application that leverages AI-powered facial recognition to help find missing persons. Citizens can report a missing person with a photo, and law enforcement officers can use a **live camera scan** to match faces in real-time against a database of reported cases. When a match is found, the system automatically alerts the complainant via **WhatsApp** and provides an **AI chatbot** for guidance.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **Database** | SQLite3 |
| **Face Recognition** | DeepFace (ArcFace model), OpenCV |
| **AI Chatbot** | Google Gemini 2.5 Flash API |
| **WhatsApp Alerts** | Twilio Messaging API |
| **Frontend** | Jinja2 Templates, HTML5/CSS3, JavaScript, Chart.js |
| **Deployment** | Render (Web Service) |

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser)                         │
│   Landing Page  │  Report Form  │  Officer Dashboard  │ Chatbot  │
└────────┬────────┴───────┬───────┴──────────┬──────────┴────┬─────┘
         │                │                  │               │
         ▼                ▼                  ▼               ▼
┌──────────────────────────────────────────────────────────────────┐
│                     FastAPI Application (ASGI)                   │
│                                                                  │
│  ┌─────────────┐ ┌────────────┐ ┌─────────────┐ ┌────────────┐  │
│  │  Landing     │ │  Report    │ │  Officer    │ │  Chat      │  │
│  │  Router      │ │  Router    │ │  Router     │ │  Router    │  │
│  └──────┬──────┘ └─────┬──────┘ └──────┬──────┘ └─────┬──────┘  │
│         │              │               │              │          │
│  ┌──────┴──────────────┴───────────────┴──────────────┴──────┐   │
│  │                     SERVICE LAYER                         │   │
│  │                                                           │   │
│  │  ┌──────────────────┐  ┌──────────────────────────────┐   │   │
│  │  │  Case Service    │  │  Face Recognition Service    │   │   │
│  │  │  (CRUD ops)      │  │  (DeepFace + ArcFace)        │   │   │
│  │  └──────────────────┘  └──────────────────────────────┘   │   │
│  │  ┌──────────────────┐  ┌──────────────────────────────┐   │   │
│  │  │  Gemini Service  │  │  WhatsApp Service            │   │   │
│  │  │  (AI Chatbot)    │  │  (Twilio Alerts)             │   │   │
│  │  └──────────────────┘  └──────────────────────────────┘   │   │
│  └───────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌───────────────────────────┴───────────────────────────────┐   │
│  │                     DATA LAYER                            │   │
│  │  SQLite DB (cases, comments) │ File Storage (uploads/)    │   │
│  └───────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Report Submission** → Image uploaded → DeepFace generates a 512-d ArcFace embedding → Case + embedding saved to SQLite → WhatsApp confirmation sent to complainant
2. **Live Camera Scan** → Officer captures frame from webcam → Frame embedding extracted → Cosine similarity compared against all stored embeddings → Match results displayed → WhatsApp alert sent on match
3. **Chatbot** → User query → Gemini 2.5 Flash API processes with missing-person-specific system prompt → Response returned (with intelligent mock fallback on quota limits)

---

## ✨ Key Features

### 🧑‍💻 For Citizens
- **Report a Missing Person** — Submit comprehensive details (name, age, location, description) with a photo
- **AI Chatbot** — 24/7 Gemini-powered assistant for guidance on immediate steps, how the system works, and privacy info
- **WhatsApp Notifications** — Instant confirmation on report submission + automatic alert when a match is found

### 👮 For Officers
- **Secure Dashboard** — Session-based login with case overview and analytics charts (Chart.js)
- **Live Camera Face Scan** — Real-time webcam face matching against the entire case database using DeepFace
- **Case Management** — View all cases, update statuses, add comments/notes
- **Analytics** — Visual bar charts showing case trends by date

### 🤖 AI & Recognition
- **ArcFace Model** — State-of-the-art face recognition with 512-dimensional embeddings
- **Multi-detector Fallback** — Tries OpenCV → SSD → RetinaFace for robust face detection
- **Cosine Distance Matching** — Threshold-based matching (0.55) with confidence percentage

---

## 📁 Project Structure

```
tinker-hack/
├── app/
│   ├── main.py                  # FastAPI app entry point, middleware, routers
│   ├── config.py                # Environment configuration
│   ├── models/
│   │   └── database.py          # SQLite schema & connection management
│   ├── routes/
│   │   ├── landing.py           # Home page (GET /)
│   │   ├── report.py            # Report form (GET/POST /report)
│   │   ├── officer.py           # Officer dashboard, login, camera scan
│   │   ├── comments.py          # Case comments API
│   │   └── chat.py              # Chatbot API endpoint
│   ├── services/
│   │   ├── case_service.py      # Case CRUD & analytics queries
│   │   ├── face_recognition_service.py  # DeepFace embedding & matching
│   │   ├── gemini_service.py    # Gemini AI chatbot integration
│   │   ├── whatsapp_service.py  # Twilio WhatsApp notifications
│   │   ├── openai_service.py    # OpenAI service (alternative)
│   │   └── db_chat_service.py   # Database-aware chat service
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── base.html            # Base layout with chatbot widget
│   │   ├── index.html           # Landing page
│   │   ├── report.html          # Missing person report form
│   │   ├── officer_login.html   # Officer authentication page
│   │   ├── officer_dashboard.html # Dashboard with cases & analytics
│   │   └── case_detail.html     # Individual case view
│   └── static/                  # CSS, JS, images
├── uploads/                     # Uploaded missing person photos
├── database.db                  # SQLite database file
├── requirements.txt             # Python dependencies
├── .python-version              # Python version for Render (3.11.11)
├── .env.example                 # Environment variable template
└── .gitignore
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/BabyMumthas/tinker-hack.git
cd tinker-hack

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your actual API keys (see below)

# 5. Run the application
uvicorn app.main:app --reload --port 8001
```

The app will be available at **http://localhost:8001**

---

## 🔑 Environment Variables

Create a `.env` file from `.env.example`:

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | Session encryption key | ✅ |
| `GEMINI_API_KEY` | Google Gemini API key for chatbot | ✅ |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID | For WhatsApp |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token | For WhatsApp |
| `TWILIO_FROM_WHATSAPP` | Twilio WhatsApp sender number | For WhatsApp |
| `OFFICER_PHONE` | Default officer contact number | Optional |

---

## 💡 Usage

| Route | Description |
|---|---|
| `GET /` | Landing page |
| `GET /report` | Missing person report form |
| `POST /report` | Submit a missing person report |
| `GET /officer/login` | Officer login page |
| `GET /officer/dashboard` | Officer dashboard (authenticated) |
| `POST /officer/scan-frame` | Live camera face scan API |
| `POST /chat` | AI chatbot endpoint |

---

## ☁️ Deployment

This project is configured for deployment on **Render**:

| Setting | Value |
|---|---|
| **Root Directory** | `tinker-hack` |
| **Build Command** | `pip install setuptools wheel ; pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port 10000` |
| **Python Version** | 3.11.11 (via `.python-version` file) |

> **Note:** Add all environment variables in Render's **Environment** tab — the `.env` file is not deployed.

---

## 🔮 Future Enhancements

| Enhancement | Description |
|---|---|
| 🗄️ **PostgreSQL Migration** | Replace SQLite with PostgreSQL for production-grade scalability and concurrent access |
| 📍 **GPS Location Tracking** | Add geolocation tagging when a match is spotted for precise last-seen location |
| 🔔 **Multi-channel Alerts** | Extend notifications to SMS, email, and push notifications alongside WhatsApp |
| 📊 **Advanced Analytics** | Heatmaps of missing person locations, age/gender distribution charts, recovery rate metrics |
| 🧠 **Age Progression AI** | Integrate age-progression models to match older photos against current faces |
| 📱 **Mobile App** | Flutter/React Native companion app for officers to scan on-the-go |
| 🔐 **Role-based Access** | Multi-tier authentication (admin, senior officer, field officer) with granular permissions |
| 🌐 **Multi-language Support** | Localization for Hindi, Tamil, Telugu, and other regional languages |
| 🤝 **Inter-agency Integration** | API bridge to connect with national databases (e.g., TrackChild, CCTNS) |
| 🎥 **CCTV Integration** | Continuous face scanning from CCTV feeds using edge computing |
| 📋 **Case Timeline** | Detailed activity log for each case showing all status changes and officer actions |
| 🧪 **Improved Matching** | Ensemble models combining ArcFace + FaceNet for higher accuracy across diverse conditions |

---

## 👥 Team

Built with ❤️ for **TinkHer Hack**

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
