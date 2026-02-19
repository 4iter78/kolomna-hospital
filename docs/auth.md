# Authentication & Authorization

## Authentication

### Session-Based Login

The application uses Flask's built-in session mechanism (signed cookies) for authentication.

**Login flow:**

1. User submits `POST /login` with form fields `username` and `password`
2. Server looks up the user by the `login` column in the `users` table
3. Password is hashed using PostgreSQL's `pgcrypto` extension:
   ```sql
   SELECT encode(digest(:pwd, 'sha256'), 'hex') AS h
   ```
4. The resulting hash is compared to the `hash_password` column on the user record
5. On success, the following values are stored in the Flask session:
   - `user_id` — integer primary key
   - `user_name` — formatted as `"Surname Name"`
   - `user_login` — the login string
6. The user is redirected to `/` or the `next` query parameter if present

**Important:** Password hashing happens in SQL, not in Python. The `pgcrypto` extension must be enabled in the PostgreSQL database.

### Session Enforcement

A global `@app.before_request` hook checks every incoming request:

- If `session.get('user_id')` is falsy and the endpoint is **not** `auth_controller.login` or `static`, the user is redirected to `/login?next=<original_path>`
- There is no session timeout configured — sessions last until the browser clears the cookie or the user calls `/logout`

### Logout

`GET /logout` clears the entire session and redirects to `/login`.

---

## Authorization (RBAC)

The system implements Role-Based Access Control stored entirely in the database. No roles or permissions are hardcoded.

### Database Tables

**`entities`** — Registry of protected resources:

| Column | Type        | Description            |
|--------|-------------|------------------------|
| `id`   | Integer PK  |                        |
| `code` | String(50)  | Unique identifier (e.g. `"users"`, `"patients"`, `"work_timetable"`) |
| `name` | String(100) | Human-readable name    |

**`role_permissions`** — Permission matrix:

| Column      | Type       | Description                                      |
|-------------|------------|--------------------------------------------------|
| `id`        | Integer PK |                                                  |
| `role_id`   | Integer FK | References `user_roles.id` (CASCADE delete)      |
| `entity_id` | Integer FK | References `entities.id` (CASCADE delete)        |
| `can_read`  | Boolean    | User can view this entity (default: `false`)     |
| `can_write` | Boolean    | User can create/edit/delete (default: `false`)   |
| `own_only`  | Boolean    | Restricts write to own records (default: `false`)|

A unique constraint `(role_id, entity_id)` ensures one permission row per role-entity pair.

### Permission Functions (`permissions.py`)

| Function | Signature | Returns |
|----------|-----------|---------|
| `can_read` | `(entity_code: str, role_id: int) -> bool` | Whether the role can view the entity |
| `can_write` | `(entity_code: str, role_id: int) -> bool` | Whether the role can modify the entity |
| `is_own_only` | `(entity_code: str, role_id: int) -> bool` | Whether the role is restricted to own records |
| `get_all_permissions` | `(role_id: int) -> dict` | All permissions for a role (used by admin UI) |

All functions use `_load_perm()` internally, which caches results in `flask.g._perm_cache` for the duration of a single HTTP request.

### Decorators (`decorators.py`)

#### `@login_required`

Redirects to `/login` if `session['user_id']` is not set. Largely redundant since `before_request` handles this globally, but available for explicit use.

#### `@access_control(entity_code)`

Applied to controller routes. Checks permissions based on HTTP method:

- **GET** requests → checks `can_read(entity_code, role)`
- **POST / PUT / DELETE** requests → checks `can_write(entity_code, role)`
- Returns **403** if the check fails

Example:
```python
@work_timetable_controller.route('/work_timetable', methods=['POST', 'GET'])
@access_control('work_timetable')
def handle_work_timetables():
    ...
```

#### `@access_control_with_ownership(entity_code, get_entry_owner_id)`

Extends `@access_control` with an ownership check for write operations:

1. Performs the same read/write permission check
2. For POST/PUT/DELETE, if `is_own_only()` returns `True`:
   - Extracts the entry ID from the first URL parameter
   - Calls `get_entry_owner_id(entry_id)` to get the record's owner
   - Compares the owner to `session['user_id']`
   - Returns **403** if they differ

Example:
```python
def _get_owner(entry_id):
    link = WorkTimetableToUser.query.filter_by(work_timetable_id=entry_id).first()
    return link.user_id if link else None

@work_timetable_controller.route('/work_timetable/<entry_id>', methods=['GET', 'PUT', 'DELETE'])
@access_control_with_ownership('work_timetable', _get_owner)
def handle_work_timetable(entry_id):
    ...
```

### Template Permission Injection

The `@app.context_processor` in `app.py` injects the following into every Jinja2 template:

| Variable | Type | Description |
|----------|------|-------------|
| `current_role` | `int \| None` | The user's role ID from session |
| `current_user_id` | `int \| None` | The user's ID from session |
| `can_read` | `lambda entity -> bool` | Check read permission |
| `can_write` | `lambda entity -> bool` | Check write permission |
| `is_own_only` | `lambda entity -> bool` | Check own-only restriction |

Templates use these to conditionally show navigation items, edit/delete buttons, and creation forms.

### Admin Permissions Interface

`GET /admin/permissions` displays an interactive matrix of all roles vs. all entities, with checkboxes for `can_read`, `can_write`, and `own_only`. Changes are saved via `POST /admin/permissions/update` (AJAX). Access requires `can_write('user_roles')`, effectively restricting it to administrators.
