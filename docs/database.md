# Database Schema

The application uses PostgreSQL with the `pgcrypto` extension. All models are defined in `models/` using Flask-SQLAlchemy.

## Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│  user_roles  │───┐   │ role_permissions  │   ┌───│   entities   │
│──────────────│   │   │──────────────────│   │   │──────────────│
│ id       PK  │   └──►│ role_id    FK     │   │   │ id       PK  │
│ name         │       │ entity_id  FK     │◄──┘   │ code   UQ    │
└──────┬───────┘       │ can_read          │       │ name         │
       │               │ can_write         │       └──────────────┘
       │               │ own_only          │
       │               └──────────────────┘
       │
       │
┌──────┴───────┐       ┌──────────────────┐       ┌──────────────┐
│    users     │       │   health_cards   │       │   patients   │
│──────────────│       │──────────────────│       │──────────────│
│ id       PK  │◄──┐   │ id           PK  │   ┌──►│ id       PK  │
│ surname      │   │   │ patient_id       │───┘   │ surname      │
│ name         │   │   │ create_datetime  │       │ name         │
│ second_name  │   └───│ user_id          │       │ second_name  │
│ employment_  │       └──────────────────┘       │ birth_date   │
│   date       │                                   │ birth_place  │
│ user_role_id │                                   │ phone        │
│ login        │                                   │ email        │
│ password     │       ┌──────────────────┐       │ address      │
│ hash_password│       │ work_timetable_  │       │ passport     │
└──────┬───────┘       │    to_user       │       │ oms_number   │
       │               │──────────────────│       └──────────────┘
       │           ┌──►│ work_timetable_id│
       │           │   │   FK CASCADE     │
       └───────────┼───│ user_id          │
                   │   │   FK CASCADE     │
                   │   └──────────────────┘
                   │
┌──────────────┐   │   ┌──────────────────┐       ┌──────────────┐
│work_timetable│───┘   │ clean_timetable  │       │    rooms     │
│──────────────│       │──────────────────│       │──────────────│
│ id       PK  │       │ id           PK  │   ┌──►│ id       PK  │
│ room_id      │───┐   │ user_id          │   │   │ name         │
│ work_date    │   │   │ room_id          │───┘   │ room_type_id │
│ time_from    │   │   │ clean_datetime   │       │ special_type_│
│ time_to      │   │   └──────────────────┘       │   id         │
└──────────────┘   │                               └──────┬───────┘
                   │                                       │
                   │                               ┌──────┴───────┐
                   └──────────────────────────────►│  room_type   │
                                                   │──────────────│
                                                   │ id       PK  │
                                                   │ name         │
                                                   └──────────────┘

┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ diagnosises  │    │    drugs     │    │treatment_    │
│──────────────│    │──────────────│    │   types      │
│ id       PK  │    │ id       PK  │    │──────────────│
│ name         │    │ name         │    │ id       PK  │
└──────────────┘    └──────────────┘    │ name         │
                                        └──────────────┘
```

## Tables

### user_roles

User role definitions (e.g. Administrator, Doctor, Nurse).

| Column | Type    | Constraints | Description |
|--------|---------|-------------|-------------|
| id     | Integer | PRIMARY KEY | Auto-increment |
| name   | String  |             | Role name   |

**Model:** `models/UserRoles.py`

---

### entities

Registry of protected resources for the RBAC system.

| Column | Type       | Constraints        | Description |
|--------|------------|--------------------|-------------|
| id     | Integer    | PRIMARY KEY        |             |
| code   | String(50) | UNIQUE, NOT NULL   | Lookup key (e.g. `"users"`, `"patients"`) |
| name   | String(100)| NOT NULL           | Display name |

**Relationship:** Has many `role_permissions` (cascade delete).

**Model:** `models/Entities.py`

---

### role_permissions

Permission matrix — one row per (role, entity) pair.

| Column    | Type    | Constraints                                  | Default |
|-----------|---------|----------------------------------------------|---------|
| id        | Integer | PRIMARY KEY                                  |         |
| role_id   | Integer | FK → `user_roles.id` (CASCADE), NOT NULL     |         |
| entity_id | Integer | FK → `entities.id` (CASCADE), NOT NULL       |         |
| can_read  | Boolean | NOT NULL                                     | `false` |
| can_write | Boolean | NOT NULL                                     | `false` |
| own_only  | Boolean | NOT NULL                                     | `false` |

**Unique constraint:** `(role_id, entity_id)`

**Model:** `models/RolePermissions.py`

---

### users

Hospital staff / system users.

| Column          | Type    | Constraints | Description                          |
|-----------------|---------|-------------|--------------------------------------|
| id              | Integer | PRIMARY KEY |                                      |
| surname         | String  |             | Last name                            |
| name            | String  |             | First name                           |
| second_name     | String  |             | Patronymic (middle name)             |
| employment_date | Date    |             | Date of employment                   |
| user_role_id    | Integer |             | References `user_roles.id` (no FK declared in model) |
| login           | String  |             | Login username                       |
| password        | String  |             | Plain-text password (legacy field)   |
| hash_password   | String  |             | SHA256 hash (hex-encoded)            |

**Note:** `password` and `hash_password` are excluded from `__json__()` output.

**Model:** `models/Users.py`

---

### patients

Patient personal information.

| Column      | Type    | Constraints | Description                |
|-------------|---------|-------------|----------------------------|
| id          | Integer | PRIMARY KEY |                            |
| surname     | String  |             | Last name                  |
| name        | String  |             | First name                 |
| second_name | String  |             | Patronymic                 |
| birth_date  | Date    |             | Date of birth              |
| birth_place | String  |             | Place of birth             |
| phone       | String  |             | Phone number               |
| email       | String  |             | Email address              |
| address     | Text    |             | Residential address        |
| passport    | String  |             | Passport number            |
| oms_number  | String  |             | OMS (medical insurance) number |

**Model:** `models/Patients.py`

---

### health_cards

Medical records linking patients to staff.

| Column          | Type     | Constraints | Description              |
|-----------------|----------|-------------|--------------------------|
| id              | Integer  | PRIMARY KEY |                          |
| patient_id      | Integer  |             | References `patients.id` |
| create_datetime | DateTime |             | Record creation timestamp (defaults to `datetime.now()` in controller) |
| user_id         | Integer  |             | References `users.id` (creator) |

**Model:** `models/HealthCards.py`

---

### rooms

Hospital rooms and facilities.

| Column          | Type    | Constraints      | Description              |
|-----------------|---------|------------------|--------------------------|
| id              | Integer | PRIMARY KEY      |                          |
| name            | String  |                  | Room name/number         |
| room_type_id    | Integer |                  | References `room_type.id`|
| special_type_id | Integer | NULLABLE         | Optional special classification |

**Model:** `models/Rooms.py`

---

### room_type

Room type lookup table.

| Column | Type    | Constraints | Description |
|--------|---------|-------------|-------------|
| id     | Integer | PRIMARY KEY |             |
| name   | String  |             | Type name   |

**Model:** `models/RoomType.py`

---

### work_timetable

Work schedule entries.

| Column    | Type    | Constraints | Description         |
|-----------|---------|-------------|---------------------|
| id        | Integer | PRIMARY KEY |                     |
| room_id   | Integer |             | References `rooms.id` |
| work_date | Date    |             | Schedule date       |
| time_from | Time    |             | Shift start time    |
| time_to   | Time    |             | Shift end time      |

**Model:** `models/WorkTimetable.py`

---

### work_timetable_to_user

Junction table linking work schedule entries to users (many-to-many).

| Column            | Type    | Constraints                               | Description |
|-------------------|---------|-------------------------------------------|-------------|
| id                | Integer | PRIMARY KEY                               |             |
| work_timetable_id | Integer | FK → `work_timetable.id` (CASCADE), NOT NULL |          |
| user_id           | Integer | FK → `users.id` (CASCADE), NOT NULL       |             |

This table is also used for the ownership check — when `own_only` is set, the system looks up this table to determine who owns a schedule entry.

**Model:** `models/WorkTimetableToUser.py`

---

### clean_timetable

Cleaning schedule entries.

| Column         | Type     | Constraints | Description           |
|----------------|----------|-------------|-----------------------|
| id             | Integer  | PRIMARY KEY |                       |
| user_id        | Integer  |             | References `users.id` |
| room_id        | Integer  |             | References `rooms.id` |
| clean_datetime | DateTime |             | Scheduled date/time   |

**Model:** `models/CleanTimetable.py`

---

### diagnosises

Diagnosis reference table.

| Column | Type    | Constraints | Description    |
|--------|---------|-------------|----------------|
| id     | Integer | PRIMARY KEY |                |
| name   | String  |             | Diagnosis name |

**Model:** `models/Diagnosises.py`

---

### drugs

Medication reference table.

| Column | Type    | Constraints | Description     |
|--------|---------|-------------|-----------------|
| id     | Integer | PRIMARY KEY |                 |
| name   | String  |             | Medication name |

**Model:** `models/Drugs.py`

---

### treatment_types

Treatment type reference table.

| Column | Type    | Constraints | Description         |
|--------|---------|-------------|---------------------|
| id     | Integer | PRIMARY KEY |                     |
| name   | String  |             | Treatment type name |

**Model:** `models/TreatmentTypes.py`
