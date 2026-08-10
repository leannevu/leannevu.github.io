# Leanne Vu portfolio

This repository contains the complete site deployed to Railway and served at
`https://leannevu.com`.

## Structure

- `index.html`, `assets/`, and `blog/` contain the static portfolio.
- `app.py` is the single Railway/Flask entry point.
- `projects/routes/` contains the Flask Blueprints.
- `projects/templates/` contains project pages.
- `projects/static/` contains project-specific browser assets and datasets.
- `projects/services/` contains reusable Python application logic.
- `projects/data/` contains dashboard data and saved model runs.

All interactive pages and their APIs are namespaced beneath `/projects`. The
portfolio remains available at `/`, and legacy project URLs redirect to their
new locations.

## Run locally

Create a virtual environment and install `requirements.txt`. To use the study
dashboard database locally, copy `.env.example` to `.env` and replace the
placeholder PostgreSQL URL. On Railway, configure those values as service
environment variables instead of uploading `.env`.

Then run:

```powershell
python app.py
```

Then open `http://127.0.0.1:5000/`. Railway uses the root `Procfile` and starts
the same application with Gunicorn.

Do not commit `.env`, virtual environments, credentials, or local log files.
