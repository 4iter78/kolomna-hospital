# Architecture

## Overview

The application follows a three-layer architecture with Flask blueprints, SQLAlchemy models, and Jinja2 templates. All layers are connected through a single shared SQLAlchemy instance.

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Templates   │◄────│  Controllers │────►│    Models     │
│  (Jinja2)    │     │ (Blueprints) │     │ (SQLAlchemy)  │
└─────────────┘     └──────┬───────┘     └──────┬───────┘
                           │                     │
                    ┌──────┴───────┐             │
                    │  Decorators  │             │
                    │  Permissions │             │
                    └──────────────┘      ┌──────┴───────┐
                                          │  PostgreSQL   │
                                          └──────────────┘
```

## Application Factory

`app.py` defines `create_app()` which:

1. Creates the Flask application instance
2. Configures the database URI and secret key
3. Initializes the SQLAlchemy connection (`db_connection`)
4. Registers three global hooks:
   - **`@app.before_request`** — redirects unauthenticated users to `/login` (except for the login page and static assets)
   - **`@app.context_processor`** — injects RBAC functions (`can_read`, `can_write`, `is_own_only`, `current_role`, `current_user_id`) into all templates
   - **`@app.errorhandler(403)`** — renders the custom forbidden page

## Entry Point

`run.py` is the application entry point:

1. Calls `create_app()` to get the Flask app
2. Registers all 13 controller blueprints
3. Sets a custom `ModelEncoder` as the JSON encoder (calls `__json__()` on model instances)
4. Starts the Flask dev server on port 8000

## Controllers (Blueprints)

Each entity has a dedicated controller file in `controllers/`. Every controller:

- Creates a `Blueprint` instance
- Aliases `db_connection` as `db` for convenience
- Defines two route functions following a standard CRUD pattern:
  - `/<entity>` — `GET` (list all, render HTML template) and `POST` (create, redirect)
  - `/<entity>/<id>` — `GET` (JSON detail), `PUT` (JSON update), `DELETE` (JSON delete)

List endpoints (`GET /<entity>`) render full HTML pages. Single-item endpoints (`GET/PUT/DELETE /<entity>/<id>`) return JSON — these are called from the frontend via `fetch()`.

POST requests accept either JSON or form data (`request.get_json() if request.is_json else request.form`).

## Models

All models are in `models/` and follow the same pattern:

- Import `db_connection` from `app` and alias as `db`
- Define a class extending `db.Model` with `__tablename__`
- Define columns using `db.Column(...)`
- Implement `__init__()` constructor
- Implement `__json__()` for serialization (used by `ModelEncoder`)
- Implement `__repr__()` for debugging

Foreign key relationships are not declared via SQLAlchemy `relationship()` on most models (except `Entities` → `RolePermissions`). Instead, controllers manually resolve references by querying related tables inline.

## JSON Serialization

`ModelEncoder` (defined in `run.py`) extends `json.JSONEncoder`. When Flask serializes a response, it checks if the object has a `__json__()` method and calls it. This is how model instances are converted to JSON in API responses.

## Request Lifecycle

```
Browser Request
      │
      ▼
 before_request hook
 (check session for user_id → redirect to /login if missing)
      │
      ▼
 @access_control decorator (if applied)
 (check can_read for GET, can_write for POST/PUT/DELETE → 403 if denied)
      │
      ▼
 Controller function
 (query models, build response)
      │
      ▼
 render_template() or JSON dict
      │
      ▼
 context_processor injects permissions into template
      │
      ▼
 Response to browser
```

## Permission Caching

Permissions are loaded from the database on first access per HTTP request and cached in `flask.g._perm_cache`. This means:

- No external cache (Redis/Memcached) is needed
- Changes to permissions in the database take effect on the next HTTP request
- Each request pays for at most one DB query per unique (role_id, entity_code) pair
