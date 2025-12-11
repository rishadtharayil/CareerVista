# Deployment Guide for CareerVista

CareerVista is a Django application ready for Dockerized deployment. Recommended providers: Render, Railway, or Heroku.

## Option 1: Render.com (Recommended)
1.  **Fork/Push** this repository to GitHub.
2.  Create a **Web Service** in Render from your repo.
3.  **Environment Variables**:
    *   `PYTHON_VERSION`: `3.11`
    *   `SECRET_KEY`: Generate a strong key.
    *   `DEBUG`: `False`
    *   `DATABASE_URL`: Add a **PostgreSQL** database service in Render and link it.
    *   `GEMINI_API_KEY`: Your Google Gemini API Key.
    *   `DJANGO_ALLOWED_HOSTS`: `*` (or your domain).
4.  **Build Command**:
    ```bash
    pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
    ```
5.  **Start Command**:
    ```bash
    gunicorn careervista.wsgi:application
    ```

## Option 2: Docker
You can deploy using the provided `Dockerfile`.
1.  Build image: `docker build -t careervista .`
2.  Run: `docker run -e ... -p 8000:8000 careervista`

## Option 3: Heroku
1.  Install Heroku CLI.
2.  `heroku create careervista-app`
3.  `heroku addons:create heroku-postgresql:hobby-dev`
4.  `git push heroku main`
5.  Set env vars: `heroku config:set GEMINI_API_KEY=...`

## Database Seeding
After deployment, run the seed command to populate careers:
- **Render**: Use Shell in dashboard -> `python manage.py seed_careers`
- **Heroku**: `heroku run python manage.py seed_careers`
