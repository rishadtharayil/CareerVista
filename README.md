# CareerVista

A production-ready career guidance web application powered by Gemini AI.

## Features
- **Career Catalogue**: Detailed career paths, skills, queries.
- **Roadmaps**: Step-by-step guides with resources.
- **AI Coach**: Chat with Gemini to get personalized advice.
- **Progress Tracking**: Track your learning journey.
- **REST API**: Fully documented API.

## API Documentation
The API schema is available at `/api/docs/` (Swagger UI) when running the server.

## Local Development

### Prerequisites
- Docker & Docker Compose
- OR Python 3.11+ (if running locally without Docker)

### Setup (Docker)
1.  Copy `.env.example` to `.env` and fill in keys.
2.  Run `docker-compose up --build`.
3.  Access app at `http://localhost:8000`.

### Setup (Local without Docker)
1.  `pip install -r requirements.txt`
2.  Set `DATABASE_URL=sqlite:///db.sqlite3` in `.env`.
3.  `python manage.py migrate`
4.  `python manage.py seed_careers` (Populate data)
5.  `python manage.py runserver`

## Stack
- **Backend**: Django 5, DRF
- **Database**: PostgreSQL (Prod), SQLite (Dev)
- **Frontend**: Django Templates + simple CSS (Dark Mode) + Vanilla JS
- **AI**: Google Gemini Pro

## License
MIT
