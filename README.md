[README.md]
# Engineering Learning Platform — Backend

A RESTful API backend for a multi-department engineering learning platform, built with Django REST Framework. The platform serves engineering students across five departments with structured course content, AI-generated quizzes, personalized study recommendations, and curated video resources.

---

## Features

- JWT-based user authentication and registration
- Department management across five engineering faculties (BMEN, CPEN, AREN, FPEN, MTEN)
- Level system (100–400) with pre-seeded Level 100 courses per department
- Admin-managed courses for Levels 200–400
- AI-generated quizzes per course via the Anthropic Claude API
- Automated quiz result analysis with personalized study plans
- Curated video resource links per course
- Full Django Admin panel for content management

---

## Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Language     | Python 3.11+                        |
| Framework    | Django 4.2+                         |
| API Layer    | Django REST Framework               |
| Database     | PostgreSQL 15                       |
| Auth         | Simple JWT (djangorestframework-simplejwt) |
| AI           | Anthropic Claude API                |
| Cache        | Redis (optional, for rate limiting) |
| Config       | python-decouple / `.env`            |
| Testing      | pytest + pytest-django              |

---

## Project Structure

```
esug_platform/
├── config/               # Django project settings and root URLs
├── accounts/             # User registration, JWT auth, profiles
├── departments/          # Departments and academic levels
├── courses/              # Courses, video resources, Level 100 seed command
├── quizzes/              # AI quiz generation, questions, options
├── results/              # Quiz attempts, scoring, AI recommendations
├── manage.py
├── requirements.txt
└── .env
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15
- Redis (optional but recommended)
- Git

### 1. Clone and set up the environment

```bash
git clone <repo-url>
cd engineering_platform

python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 2. Configure environment variables

Copy the example below into a `.env` file at the project root. **Never commit this file.**

```env
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=engineering_platform
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

ANTHROPIC_API_KEY=sk-ant-your-key-here

JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

### 3. Create the PostgreSQL database

```sql
psql -U postgres
CREATE DATABASE esug_platform;
CREATE USER enguser WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE esug_platform TO enguser;
\q
```

### 4. Run migrations in dependency order

```bash
python manage.py makemigrations accounts
python manage.py makemigrations departments
python manage.py makemigrations courses
python manage.py makemigrations quizzes
python manage.py makemigrations results
python manage.py migrate
```

### 5. Seed Level 100 courses

```bash
python manage.py seed_level100
```

This populates the database with the fixed Level 100 curriculum for all departments.

### 6. Create a superuser and start the server

```bash
python manage.py createsuperuser
python manage.py runserver
```

- **API Root:** `http://localhost:8000/api/`
- **Admin Panel:** `http://localhost:8000/admin/`

---

## Level 100 Course Rules

| Applies To              | Courses                                                                 |
|-------------------------|-------------------------------------------------------------------------|
| All departments         | Calculus 1, Statics for Mechanics, Introduction to Engineering, General Physics |
| All departments except CPEN | Chemistry                                                          |
| CPEN only               | Computer Innovations                                                    |

Levels 200–400 courses are added exclusively through the Django Admin panel by staff or superusers.

---

## API Endpoints

### Authentication

| Method | Endpoint                   | Auth | Description               |
|--------|----------------------------|------|---------------------------|
| POST   | `/api/auth/register/`      | No   | Register a new user       |
| POST   | `/api/auth/login/`         | No   | Login and receive tokens  |
| POST   | `/api/auth/token/refresh/` | No   | Refresh access token      |
| POST   | `/api/auth/logout/`        | Yes  | Blacklist refresh token   |
| GET    | `/api/auth/profile/`       | Yes  | Retrieve own profile      |
| PATCH  | `/api/auth/profile/`       | Yes  | Update own profile        |

### Departments & Levels

| Method | Endpoint               | Auth | Description           |
|--------|------------------------|------|-----------------------|
| GET    | `/api/departments/`    | Yes  | List all departments  |
| GET    | `/api/departments/{id}/` | Yes | Get one department  |
| GET    | `/api/levels/`         | Yes  | List all levels       |

### Courses & Videos

| Method     | Endpoint            | Auth       | Description                    |
|------------|---------------------|------------|--------------------------------|
| GET        | `/api/courses/`     | Yes        | List courses (filterable)      |
| POST       | `/api/courses/`     | Admin only | Create a course                |
| GET        | `/api/courses/{id}/`| Yes        | Course detail with videos      |
| PUT/PATCH  | `/api/courses/{id}/`| Admin only | Update course                  |
| DELETE     | `/api/courses/{id}/`| Admin only | Delete course                  |
| GET        | `/api/videos/`      | Yes        | List video resources           |
| POST       | `/api/videos/`      | Admin only | Add a video resource           |

Filter courses by level or department:
```
GET /api/courses/?level__number=100
GET /api/courses/?department__code=CPEN
```

### Quizzes

| Method | Endpoint                   | Auth       | Description                    |
|--------|----------------------------|------------|--------------------------------|
| GET    | `/api/quizzes/`            | Yes        | List published quizzes         |
| GET    | `/api/quizzes/{id}/`       | Yes        | Full quiz with questions       |
| POST   | `/api/quizzes/generate/`   | Admin only | Trigger AI quiz generation     |
| PATCH  | `/api/quizzes/{id}/`       | Admin only | Update or publish a quiz       |
| DELETE | `/api/quizzes/{id}/`       | Admin only | Delete a quiz                  |

**Generate a quiz:**
```json
POST /api/quizzes/generate/
{
  "course_id": 1,
  "difficulty": "medium",
  "num_questions": 10
}
```

### Results & Recommendations

| Method | Endpoint                                    | Auth | Description                       |
|--------|---------------------------------------------|------|-----------------------------------|
| POST   | `/api/results/attempts/`                    | Yes  | Start a quiz attempt              |
| GET    | `/api/results/attempts/`                    | Yes  | List own attempts                 |
| GET    | `/api/results/attempts/{id}/`               | Yes  | Get attempt detail                |
| POST   | `/api/results/attempts/{id}/submit/`        | Yes  | Submit answers and trigger AI     |
| GET    | `/api/results/attempts/{id}/recommendation/`| Yes  | Get AI-generated study plan       |

**Submit answers:**
```json
POST /api/results/attempts/{id}/submit/
{
  "answers": [
    { "question_id": 1, "option_id": 3 },
    { "question_id": 2, "option_id": 7 }
  ]
}
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pip install pytest-cov
pytest --cov=. --cov-report=html

# Run tests for a specific app
pytest accounts/
pytest courses/
pytest quizzes/
pytest results/
```

Configure `pytest.ini` at the project root:
```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = tests.py test_*.py *_tests.py
addopts = -v --tb=short
```

---

## Deployment

### Collect static files

```bash
python manage.py collectstatic --noinput
```

### Run with Gunicorn

```bash
pip install gunicorn
gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120
```

### Production checklist

- Set `DEBUG=False` in `.env`
- Use a strong, unique `SECRET_KEY` (50+ characters)
- Set `ALLOWED_HOSTS` to your actual domain
- Enable `SECURE_SSL_REDIRECT=True`
- Use a managed PostgreSQL service (AWS RDS, Supabase, Railway)
- Serve via nginx as a reverse proxy in front of Gunicorn
- Store all secrets as environment variables — never hardcode them
- Change `/admin/` to a non-obvious path in production
- Set `CORS_ALLOWED_ORIGINS` to your specific frontend domain only

---

## License

This project is a private engineering reference implementation. See your organization's licensing terms for distribution and usage rights.
