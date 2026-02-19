# API Reference

All routes except `/login`, `/logout`, and `/static` require an authenticated session. Unauthenticated requests are redirected to `/login`.

**Common patterns:**

- **List endpoints** (`GET /<entity>`) return an HTML page rendered from a Jinja2 template
- **Create endpoints** (`POST /<entity>`) accept either JSON or form data, create a record, and redirect to the list page
- **Detail endpoints** (`GET /<entity>/<id>`) return JSON
- **Update endpoints** (`PUT /<entity>/<id>`) accept a JSON body and return JSON
- **Delete endpoints** (`DELETE /<entity>/<id>`) return JSON

All JSON success responses follow this pattern:
```json
{"message": "...success message..."}
```

Detail GET responses follow this pattern:
```json
{"message": "success", "<entity_name>": { ...fields... }}
```

---

## Authentication

**Controller:** `controllers/AuthController.py`

### POST /login

Authenticate a user.

**Request body** (form data):

| Field      | Required | Description |
|------------|----------|-------------|
| `username` | Yes      | User login  |
| `password` | Yes      | Password    |

**Behavior:**
- On success: sets session cookies and redirects to `/` (or `?next=` param)
- On failure: re-renders login page with flash error message

### GET /login

Renders the login form. If already authenticated, redirects to `/`.

### GET /logout

Clears the session and redirects to `/login`.

---

## Home

**Controller:** `controllers/MainController.py`

### GET /

Renders the main dashboard page (`main_page.html`).

---

## User Roles

**Controller:** `controllers/UserRolesController.py`

### GET /user-roles

Renders the roles management page.

**Template variables:** `user_roles` (list of `{id, name}`), `count`

### POST /user-roles

Create a new role.

| Field  | Required | Type   |
|--------|----------|--------|
| `name` | Yes      | String |

**Response:** Redirect to `/user-roles`

### GET /user-roles/\<id\>

**Response:**
```json
{"message": "success", "user_role": {"name": "..."}}
```

### PUT /user-roles/\<id\>

| Field  | Required | Type   |
|--------|----------|--------|
| `name` | Yes      | String |

### DELETE /user-roles/\<id\>

Deletes the role.

---

## Users (Staff)

**Controller:** `controllers/UsersController.py`

### GET /users

Renders the staff management page.

**Template variables:** `users` (list of `{id, surname, name, second_name, fio, employment_date, user_role_id, user_role}`), `user_roles`, `count`

### POST /users

Create a new staff member.

| Field             | Required | Type    |
|-------------------|----------|---------|
| `surname`         | Yes      | String  |
| `name`            | Yes      | String  |
| `second_name`     | Yes      | String  |
| `employment_date` | Yes      | Date    |
| `user_role_id`    | Yes      | Integer |

**Response:** Redirect to `/users`

### GET /users/\<id\>

**Response:**
```json
{
  "message": "success",
  "user": {
    "id": 1,
    "surname": "...",
    "name": "...",
    "second_name": "...",
    "employment_date": "...",
    "user_role": "..."
  }
}
```

### PUT /users/\<id\>

Same fields as POST.

### DELETE /users/\<id\>

Deletes the staff member.

---

## Patients

**Controller:** `controllers/PatientsController.py`

### GET /patients

Renders the patients management page.

**Template variables:** `patients` (list with all fields + computed `fio`), `count`

### POST /patients

Create a new patient.

| Field         | Required | Type   |
|---------------|----------|--------|
| `surname`     | Yes      | String |
| `name`        | Yes      | String |
| `second_name` | No       | String |
| `birth_date`  | Yes      | Date   |
| `birth_place` | No       | String |
| `phone`       | No       | String |
| `email`       | No       | String |
| `address`     | No       | String |
| `passport`    | No       | String |
| `oms_number`  | No       | String |

**Response:** Redirect to `/patients`

### GET /patients/\<id\>

Returns all patient fields as JSON.

### PUT /patients/\<id\>

Same fields as POST.

### DELETE /patients/\<id\>

Deletes the patient.

---

## Health Cards

**Controller:** `controllers/HealthCardsController.py`

### GET /health_cards

Renders the health cards page with resolved patient and user names.

**Template variables:** `health_cards` (list of `{id, patient_id, patient, create_datetime, user_id, user}`), `patients` (list of `{id, fio}`), `users` (list of `{id, fio}`), `count`

### POST /health_cards

Create a new health card.

| Field             | Required | Type     | Default           |
|-------------------|----------|----------|-------------------|
| `patient_id`      | Yes      | Integer  |                   |
| `user_id`         | Yes      | Integer  |                   |
| `create_datetime` | No       | DateTime | `datetime.now()`  |

**Response:** Redirect to `/health_cards`

### GET /health_cards/\<id\>

Returns health card with resolved patient and user names.

### PUT /health_cards/\<id\>

| Field             | Required | Type     |
|-------------------|----------|----------|
| `patient_id`      | Yes      | Integer  |
| `user_id`         | Yes      | Integer  |
| `create_datetime` | No       | DateTime |

### DELETE /health_cards/\<id\>

Deletes the health card.

---

## Work Timetable

**Controller:** `controllers/WorkTimetableController.py`

**Access control:** `@access_control('work_timetable')` on list/create route, `@access_control_with_ownership('work_timetable', _get_owner)` on detail routes.

### GET /work_timetable

Renders the work schedule page. If the user has `own_only` restriction, only their own schedules are shown (filtered via `work_timetable_to_user` junction table).

**Template variables:** `work_timetable` (list of `{id, room_id, room, work_date, time_from, time_to, user_id}`), `rooms`, `count`

### POST /work_timetable

Create a new schedule entry. Automatically links to the current user via `work_timetable_to_user`.

| Field       | Required | Type   |
|-------------|----------|--------|
| `room_id`   | Yes      | Integer|
| `work_date` | Yes      | Date   |
| `time_from` | Yes      | Time   |
| `time_to`   | Yes      | Time   |

**Response:** Redirect to `/work_timetable`

### GET /work_timetable/\<id\>

Returns schedule entry with resolved room name.

### PUT /work_timetable/\<id\>

Same fields as POST. Subject to ownership check.

### DELETE /work_timetable/\<id\>

Deletes the junction table link first, then the schedule entry. Subject to ownership check.

---

## Cleaning Timetable

**Controller:** `controllers/CleanTimetableController.py`

### GET /clean_timetable

Renders the cleaning schedule page with resolved user and room names.

**Template variables:** `clean_timetable` (list of `{id, user_id, user, room_id, room, clean_datetime}`), `users` (list of `{id, fio}`), `rooms`, `count`

### POST /clean_timetable

| Field            | Required | Type     |
|------------------|----------|----------|
| `user_id`        | Yes      | Integer  |
| `room_id`        | Yes      | Integer  |
| `clean_datetime` | Yes      | DateTime |

**Response:** Redirect to `/clean_timetable`

### GET /clean_timetable/\<id\>

### PUT /clean_timetable/\<id\>

Same fields as POST.

### DELETE /clean_timetable/\<id\>

---

## Rooms

**Controller:** `controllers/RoomsController.py`

### GET /rooms

Renders the rooms page with resolved room type names.

**Template variables:** `rooms` (list of `{id, name, room_type_id, room_type, special_type_id}`), `room_types`, `count`

### POST /rooms

| Field             | Required | Type    |
|-------------------|----------|---------|
| `name`            | Yes      | String  |
| `room_type_id`    | Yes      | Integer |
| `special_type_id` | No       | Integer |

**Response:** Redirect to `/rooms`

### GET /rooms/\<id\>

### PUT /rooms/\<id\>

Same fields as POST.

### DELETE /rooms/\<id\>

---

## Room Types

**Controller:** `controllers/RoomTypeController.py`

### GET /room_type

Renders the room types page.

**Template variables:** `room_types` (list of `{id, name}`), `count`

### POST /room_type

| Field  | Required | Type   |
|--------|----------|--------|
| `name` | Yes      | String |

### GET /room_type/\<id\>

### PUT /room_type/\<id\>

### DELETE /room_type/\<id\>

---

## Diagnoses

**Controller:** `controllers/DiagnosisesController.py`

### GET /diagnosises

Renders the diagnoses page.

**Template variables:** `diagnosises` (list of `{id, name}`), `count`

### POST /diagnosises

| Field  | Required | Type   |
|--------|----------|--------|
| `name` | Yes      | String |

### GET /diagnosises/\<id\>

### PUT /diagnosises/\<id\>

### DELETE /diagnosises/\<id\>

---

## Drugs

**Controller:** `controllers/DrugsController.py`

### GET /drugs

Renders the drugs page.

**Template variables:** `drugs` (list of `{id, name}`), `count`

### POST /drugs

| Field  | Required | Type   |
|--------|----------|--------|
| `name` | Yes      | String |

### GET /drugs/\<id\>

### PUT /drugs/\<id\>

### DELETE /drugs/\<id\>

---

## Treatment Types

**Controller:** `controllers/TreatmentTypesController.py`

### GET /treatment_types

Renders the treatment types page.

**Template variables:** `treatment_types` (list of `{id, name}`), `count`

### POST /treatment_types

| Field  | Required | Type   |
|--------|----------|--------|
| `name` | Yes      | String |

### GET /treatment_types/\<id\>

### PUT /treatment_types/\<id\>

### DELETE /treatment_types/\<id\>

---

## Admin — Permissions Matrix

**Controller:** `controllers/PermissionsController.py`

**Access control:** `@access_control('user_roles')` — requires write access to user_roles entity (admin only).

### GET /admin/permissions

Renders the interactive permissions matrix showing all roles vs. all entities with checkboxes.

**Template variables:** `roles`, `entities`, `matrix` (dict: `{role_id: {entity_code: {can_read, can_write, own_only, perm_id}}}`)

### POST /admin/permissions/update

Update a single cell in the permission matrix.

**Request body** (JSON):

| Field       | Required | Type    | Values                                  |
|-------------|----------|---------|-----------------------------------------|
| `role_id`   | Yes      | Integer |                                         |
| `entity_id` | Yes      | Integer |                                         |
| `field`     | Yes      | String  | `"can_read"`, `"can_write"`, `"own_only"` |
| `value`     | Yes      | Boolean |                                         |

**Success response:**
```json
{"ok": true, "role_id": 1, "entity_id": 2, "field": "can_read", "value": true}
```

**Error response (400):**
```json
{"error": "Invalid field"}
```
