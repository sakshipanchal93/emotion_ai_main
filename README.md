# Task Optimizer

Task Optimizer is a full-stack AI system that detects employee mood and emotion, recommends suitable tasks, tracks mood history, and provides team analytics with stress alerts.

## Tech Stack

- Frontend: React + TypeScript + Vite + Recharts
- Backend: Flask + SQLAlchemy
- AI: Text sentiment analysis (TextBlob), webcam emotion heuristic using OpenCV (extensible)
- Database: SQLite (default, presentation-ready) or PostgreSQL

## Features

- Real-time emotion detection (text + webcam endpoint)
- Task recommendation based on emotion
- Historical mood tracking per employee
- Stress management alerts for consecutive stressed streaks
- Team mood analytics dashboard
- Privacy-aware design (employee IDs only, no PII required)

## Project Structure

- `backend/` Flask API service and AI logic
- `frontend/` React dashboard
- `docker-compose.yml` optional PostgreSQL setup

## Backend Setup

1. Configure environment:
   - Copy `backend/.env.example` to `backend/.env`
2. Create virtual environment and install dependencies:
   - `cd backend`
   - `python -m venv .venv`
   - `.venv\Scripts\activate`
   - `pip install -r requirements.txt`
3. Run API:
   - `python -m app.main`

Optional PostgreSQL mode:
- Start database with `docker compose up -d` (if Docker is installed)
- Set `DATABASE_URL` in `backend/.env` to your PostgreSQL URL

API base URL: `http://localhost:8000/api/v1`

## Frontend Setup

1. Configure environment:
   - Copy `frontend/.env.example` to `frontend/.env`
2. Install and run:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

App URL: `http://localhost:5173`

## Main API Endpoints

- `POST /api/v1/emotion/detect` (text sentiment)
- `POST /api/v1/emotion/detect/webcam` (base64 image)
- `GET /api/v1/employees/{employee_id}/mood-history`
- `GET /api/v1/teams/{team_id}/analytics`
- `GET /api/v1/alerts`
- `GET /api/v1/health`

## Privacy Notes

- Use anonymized `employee_id` and `team_id` identifiers.
- Do not send personal identifiers in text payloads.
- Store only required operational data.
