Personalized Treatment App
RemedyLabBackBone – FastAPI Backend Documentation
 Overview
RemedyLabBackBone is the FastAPI-based backend service for the RemedyLab app. It manages authentication, patient and doctor records, health report uploads, AI-generated recommendations, and doctor validations.
The backend uses FastAPI + PostgreSQL + SQLAlchemy and provides RESTful APIs consumed by the macOS/iOS frontend.

 Features
✅ Doctor & Patient Signup/Login APIs
✅ Health Report Upload & Download
✅ Doctor and Patient Dashboard Data APIs
✅ AI Recommendation Generation and Storage
✅ Secure PostgreSQL Database with SQLAlchemy ORM

 Project Structure
app/
├── main.py                # FastAPI entry point
├── models/                # SQLAlchemy ORM models
├── schemas/               # Pydantic schemas
├── db/                    # Database config & session management
├── routers/               # API route definitions
├── services/              # Business logic & helper functions
├── utils/                 # Utility functions
└── requirements.txt       # Python dependencies

Key Folders
models/ → Contains models (Doctor, Patient, Report)
schemas/ → Pydantic models for request/response validation
routers/ → Defines API endpoints (auth.py, doctor.py, patient.py, health_report.py, recommendation.py)
services/ → Business logic for authentication, report handling, and AI integration
db/ → database.py for SQLAlchemy engine and session


⚙️ Tech Stack
FastAPI – API Framework
PostgreSQL – Database
SQLAlchemy – ORM for database models
Pydantic – Data validation
Uvicorn – ASGI Server

🚀 Setup Instructions
1️⃣ Clone the Repository
git clone <repo-url>
cd RemedyLabBackBone
2️⃣ Create Virtual Environment & Install Dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3️⃣ Setup PostgreSQL Database
createdb remedylab_db
4️⃣ Run the Server
uvicorn app.main:app --reload

