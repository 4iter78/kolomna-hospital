# Frontend

## Template System

All pages use Jinja2 templates. The base layout is `templates/main.html`, which provides:

- Fixed sidebar (240px) with navigation and user info
- Main content area with page header and content card
- Flash message rendering (Bootstrap alerts)
- Decorative SVG background elements

### Template Hierarchy

```
main.html (base layout)
├── main_page.html        — Dashboard / home page
├── users.html            — Staff management
├── roles.html            — Role management
├── patients.html         — Patient management
├── health_cards.html     — Health card management
├── work_timetable.html   — Work schedule
├── clean_timetable.html  — Cleaning schedule
├── rooms.html            — Room management
├── room_type.html        — Room type reference
├── treatment_types.html  — Treatment type reference
├── diagnosises.html      — Diagnosis reference
├── drugs.html            — Drug reference
├── permissions.html      — Admin permissions matrix
└── 403.html              — Access denied page

login.html (standalone — does not extend main.html)
```

### Template Blocks

Templates extend `main.html` and override:

- `{% block content %}` — page body content
- `{% block scripts %}` — additional page-specific JavaScript

### Permission-Based Rendering

Templates use the injected permission functions to conditionally render UI elements:

```jinja2
{% if can_read('users') %}
    <a href="/users">Staff</a>
{% endif %}

{% if can_write('patients') %}
    <button onclick="openModal()">Add Patient</button>
{% endif %}
```

## Sidebar Navigation

The sidebar groups links into sections:

| Section                   | Links                              |
|---------------------------|------------------------------------|
| Staff (Персонал)          | Users, Roles                       |
| Patients (Пациенты)       | Patients, Health Cards             |
| Schedule (Расписание)     | Work Timetable, Cleaning Timetable |
| References (Справочники)  | Rooms, Room Types, Treatment Types, Diagnoses, Drugs |
| Admin                     | Permissions (visible to admins)    |

The sidebar footer shows the current user's name and a logout link.

---

## CSS Design System

Styles are split into two files in `static/css/`:

### base.css

Main application stylesheet. Defines CSS custom properties:

| Variable         | Value     | Usage               |
|------------------|-----------|---------------------|
| `--blue-deep`    | `#0a2d5e` | Sidebar background  |
| `--blue-mid`     | `#1a56a0` | Primary color       |
| `--blue-light`   | `#2d7dd2` | Links, accents      |
| `--blue-pale`    | `#e8f1fb` | Light backgrounds   |
| `--accent`       | `#0099cc` | Buttons, highlights |
| `--white`        | `#ffffff` |                     |
| `--gray-light`   | `#f4f7fb` | Content background  |
| `--gray-border`  | `#cdd8e8` | Table/card borders  |
| `--text-main`    | `#1a2b3c` | Primary text        |
| `--text-muted`   | `#5a7a99` | Secondary text      |
| `--danger`       | `#d93025` | Delete actions       |
| `--success`      | `#1a7f4b` | Success messages     |
| `--sidebar-w`    | `240px`   | Sidebar width       |

**Typography:**
- Headings: Montserrat (weights 400, 500, 600, 700)
- Body text: Source Sans 3 (weights 300, 400, 600)

**Key components:**
- `.sidebar` — fixed left navigation panel
- `.main-area` — flex content area (with `fadeUp` entrance animation)
- `.content-card` — white card container for page content (with `cardIn` animation)
- `.table` — styled Bootstrap table with rounded corners and custom borders
- `.modal-overlay` / `.modal-box` — modal dialog system with animations
- `.btn-action` — action buttons (`.btn-create`, `.btn-edit`, `.btn-delete`)
- `.form-control` — input fields with blue focus border
- `.alert` — notification banners (`.alert-success`, `.alert-danger`)
- `.toast` — bottom-right toast notifications

**Responsive breakpoint:** `max-width: 768px` — sidebar becomes an overlay with transform transition.

### login.css

Standalone login page styles:

- `.login-card` — centered card (max-width 440px) with gradient header
- `.form-control` — inputs with left icon offset (42px padding)
- `.btn-login` — full-width gradient button

---

## JavaScript Utilities

`static/js/app.js` provides shared functions used across all pages:

### Modal Management

```javascript
openModal(id)           // Opens modal by ID (default: 'modal-create')
closeModal(id)          // Closes modal by ID (default: 'modal-create')
closeOnOverlay(e, id)   // Closes modal when clicking outside the dialog
```

The ESC key closes all open modals (via global `keydown` listener).

### Toast Notifications

```javascript
showToast(msg, type)    // Shows a toast notification
                        // type: 'success' (default) or 'error'
                        // Auto-removes after 3 seconds
```

### CRUD Operations

```javascript
deleteRecord(url, id)
// Shows confirmation dialog ("Удалить запись #<id>?")
// Sends DELETE request to url + id
// On success: shows toast, reloads page after 800ms

submitEdit(url, formId, modalId)
// Collects form data from formId
// Extracts 'id' field, sends PUT to url + id with remaining fields as JSON
// On success: shows toast, closes modal, reloads page after 800ms
```

### Usage in Templates

Templates call these functions from inline event handlers:

```html
<!-- Delete button -->
<button onclick="deleteRecord('/patients/', {{ p.id }})">Delete</button>

<!-- Edit form submission -->
<button onclick="submitEdit('/patients/', 'form-edit', 'modal-edit')">Save</button>

<!-- Open create modal -->
<button onclick="openModal('modal-create')">Add</button>
```

## External Dependencies (CDN)

| Resource         | CDN Source      |
|------------------|-----------------|
| Bootstrap 5.0.1  | jsDelivr        |
| Montserrat font  | Google Fonts    |
| Source Sans 3    | Google Fonts    |
