# Daily Task Management Backend

Django REST API for a personal task manager. The backend provides email-based user registration and login, JWT authentication, and CRUD operations for tasks.

The React client in [`../task_frontend`](../task_frontend) consumes the API under the `/api/` prefix.

## Features

- Custom user model with email as the login identifier.
- Password hashing through Django's password hashers.
- Short-lived JWT access tokens and longer-lived refresh tokens.
- Owner-scoped task operations: a user can only read or change their own tasks.
- Task statuses: `pending`, `in_progress`, and `completed`.
- Optional task descriptions and due dates.
- Django admin and standard migration support.
- CORS configuration for local Vite development and the deployed frontend.

## Technology stack

- Python 3.10+
- Django 5.2.7
- Django REST Framework 3.16.1
- `djangorestframework-simplejwt` for JWT authentication
- MySQL, accessed through PyMySQL
- `django-cors-headers`
- Gunicorn for production WSGI serving

## Project layout

```text
task_backend/
├── manage.py
├── requirements.txt
├── task_manager/
│   ├── settings.py       # database, JWT, CORS, installed apps
│   ├── urls.py           # project URL routing
│   ├── wsgi.py           # WSGI entry point
│   └── asgi.py           # ASGI entry point
├── users/
│   ├── models.py         # UserProfile and manager
│   ├── serializer.py     # registration/profile serialization
│   ├── views.py          # authentication API views
│   └── urls.py
├── tasks/
│   ├── models.py         # Task model
│   ├── serializer.py
│   ├── views.py          # task API
│   └── urls.py
├── pages/                # API root status endpoint
└── */migrations/         # database migrations
```

## Requirements

- Python 3.10 or newer.
- A running MySQL instance and a database created for this project.
- `pip` and a virtual-environment tool.

The project is configured for MySQL only; it does not provide a SQLite fallback. PyMySQL is installed as Django's MySQLdb-compatible driver by `task_manager/__init__.py` and `settings.py`.

## Local setup

From the backend directory:

```bash
cd task_backend
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a file named `.env` in `task_backend/` (it is ignored by Git):

```dotenv
SECRET_KEY=replace-with-a-long-random-secret

DB_NAME=task_manager
DB_USER=task_manager_user
DB_PASSWORD=replace-with-the-database-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Create the MySQL database and grant the configured user access to it, then apply migrations:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

The API is then available at `http://127.0.0.1:8000`. The React frontend should use `http://127.0.0.1:8000/api/` as its API base URL.

## Management commands

```bash
python manage.py check             # validate Django configuration
python manage.py test              # run project tests
python manage.py makemigrations    # create migrations after model changes
python manage.py migrate           # apply migrations
python manage.py collectstatic     # collect static assets for deployment
```

The current app test modules contain Django's default placeholders, so `test` is a smoke check rather than a comprehensive behavior suite.

## Authentication

REST Framework defaults all endpoints to JWT authentication and `IsAuthenticated`. Public authentication endpoints explicitly opt out of that default.

Send the access token on protected requests:

```http
Authorization: Bearer <access-token>
```

Token lifetimes configured in `settings.py`:

- Access token: 1 hour
- Refresh token: 7 days

The refresh endpoint returns a new access token. Logging out flushes the Django session; JWTs are not blacklisted, so clients should discard both tokens when logging out.

## API reference

All API URLs below are relative to `http://127.0.0.1:8000/api/`.

### Users

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `/users/register/` | Public | Create a user from `name`, `email`, and `password`. Returns `201` and a success message. |
| `POST` | `/users/login/` | Public | Verify credentials and return the serialized user, `access_token`, and `refresh_token`. |
| `POST` | `/users/token/refresh/` | Public with refresh token | Exchange `{ "refresh": "<refresh-token>" }` for a new access token. |
| `GET` | `/users/login/test/` | Public | Authentication-route smoke test. |
| `POST` | `/users/logout/` | JWT required | Flush the Django session and return a logout message. |

Example registration:

```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H 'Content-Type: application/json' \
  -d '{"name":"Ada Lovelace","email":"ada@example.com","password":"use-a-strong-password"}'
```

Example login response:

```json
{
  "message": "Login success",
  "user": {
    "id": 1,
    "name": "Ada Lovelace",
    "email": "ada@example.com",
    "date_created": "2025-10-20T09:00:00Z"
  },
  "access_token": "<jwt>",
  "refresh_token": "<jwt>"
}
```

Login returns `401` for an incorrect password and `404` when no account exists for the supplied email. Registration validation errors return `400`.

### Tasks

Every task endpoint requires a valid access token. Querysets are filtered by the authenticated user, so task IDs belonging to another user behave as not found.

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/tasks/create/` | Create a task owned by the authenticated user. |
| `GET` | `/tasks/all/` | List the authenticated user's tasks. |
| `GET` | `/tasks/<id>/` | Retrieve one owned task. |
| `PUT` | `/tasks/update/<id>/` | Partially update an owned task (the view uses `partial=True`). |
| `DELETE` | `/tasks/delete/<id>/` | Delete an owned task. |
| `PATCH` | `/tasks/complete/<id>/` | Set an owned task's status to `completed`. |

Task fields:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | Auto-generated primary key. |
| `title` | string | Required, maximum 255 characters. |
| `description` | string or `null` | Optional. |
| `due_date` | `YYYY-MM-DD` or `null` | Optional date. |
| `status` | string | `pending` (default), `in_progress`, or `completed`. |
| `date_created` | ISO 8601 datetime | Set by the server when the task is created. |

The `user` foreign key is assigned from the JWT identity and must not be supplied by the client.

Example task creation and completion:

```bash
curl -X POST http://127.0.0.1:8000/api/tasks/create/ \
  -H 'Authorization: Bearer <access-token>' \
  -H 'Content-Type: application/json' \
  -d '{"title":"Plan the week","description":"Review priorities","due_date":"2026-09-01","status":"pending"}'

curl -X PATCH http://127.0.0.1:8000/api/tasks/complete/1/ \
  -H 'Authorization: Bearer <access-token>'
```

Successful creation returns `201`, reads and updates return `200`, completion returns `200`, and deletion is intended to return `204`. Invalid payloads return `400`; an inaccessible or missing task returns `404`; an unauthenticated request returns `401`.

## API root

`GET /` returns a small JSON status response. The backend has no server-rendered HTML routes; the React application in [`../task_frontend`](../task_frontend) is the frontend client.

## Configuration and deployment

Important settings in `task_manager/settings.py`:

- `AUTH_USER_MODEL = 'users.UserProfile'`.
- `REST_FRAMEWORK` uses `JWTAuthentication` and `IsAuthenticated` by default.
- CORS is restricted to the local Vite origins and `https://daily-task-management-app.vercel.app`.
- `ALLOWED_HOSTS` includes localhost and the deployed Render/Vercel hosts.
- WSGI application: `task_manager.wsgi:application`.

Example Gunicorn command:

```bash
gunicorn task_manager.wsgi:application --bind 0.0.0.0:$PORT
```

Before production deployment:

1. Set `DEBUG = False` and provide a strong, private `SECRET_KEY`.
2. Set `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and `CSRF_TRUSTED_ORIGINS` to the actual domains only.
3. Use HTTPS. The current settings mark CSRF and session cookies as secure and `SameSite=None`.
4. Run migrations and collect static files during deployment.
5. Keep `.env` and database credentials out of source control.

## Known implementation notes

These points describe current API and integration details:

- The `user_profile` API view exists but is not included in `users/urls.py`, so there is currently no profile endpoint.
- The frontend sends a `completed` boolean for some task updates, while this backend exposes a `status` string. Use `status: "completed"` (or the dedicated completion endpoint) until the contracts are aligned.
- The frontend calls `users/forgot-password/`, but no password-reset route is defined in this backend.
- `DEBUG` is enabled in the checked-in settings and should not be used as-is in production.

## License

No license file is currently included. Add one before distributing the project if a specific reuse license is intended.
