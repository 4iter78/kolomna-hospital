# Kolomna Hospital Information System

Hospital information system for GBUZ MO Kolomna Hospital (ГБУЗ МО Коломенская больница). A web application for managing staff, patients, medical records, scheduling, and facility resources.

## Technology Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Backend  | Python, Flask, Flask-SQLAlchemy     |
| Database | PostgreSQL (with pgcrypto extension)|
| Frontend | Jinja2 templates, Bootstrap 5, vanilla JavaScript |
| Fonts    | Montserrat, Source Sans 3 (Google Fonts CDN) |

## Prerequisites

- **Python 3.x**
- **PostgreSQL** running on `localhost:54321`
- PostgreSQL `pgcrypto` extension enabled (used for SHA256 password hashing)

### Python Dependencies

| Package            | Purpose                  |
|--------------------|--------------------------|
| `flask`            | Web framework            |
| `flask-sqlalchemy`  | SQLAlchemy ORM integration |
| `psycopg2-binary`  | PostgreSQL adapter       |

Install with:

```bash
pip install flask flask-sqlalchemy psycopg2-binary
```

> Note: There is no `requirements.txt` in the repository.

## Database Setup

The application connects to PostgreSQL with the following defaults (configured in `app.py`):

- **Host:** `localhost`
- **Port:** `54321`
- **Database:** `kolomna_hospital`
- **User:** `postgres`
- **Password:** `postgres`

The database schema must already exist — the application does not run migrations automatically. Tables are defined by SQLAlchemy models in the `models/` directory.

## Running the Application

```bash
python run.py
```

The Flask development server starts on **http://localhost:8000** with debug mode enabled.

All routes except `/login` require authentication. Open the browser and log in with credentials stored in the `users` table.

## Project Structure

```
├── app.py                  # Flask app factory, middleware, context processor
├── run.py                  # Entry point — registers blueprints, starts server
├── permissions.py          # RBAC permission loading with request-scoped cache
├── decorators.py           # @access_control, @access_control_with_ownership
├── controllers/            # Flask blueprints (one per entity)
├── models/                 # SQLAlchemy ORM models
├── templates/              # Jinja2 HTML templates
└── static/
    ├── css/                # base.css, login.css
    └── js/                 # app.js (modals, toasts, CRUD helpers)
```

## Documentation Index

- [Architecture](architecture.md) — system layers, request lifecycle, app factory
- [API Reference](api.md) — all routes, methods, request/response formats
- [Database Schema](database.md) — models, columns, relationships
- [Authentication & Authorization](auth.md) — login flow, RBAC, decorators
- [Frontend](frontend.md) — templates, CSS design system, JavaScript utilities
