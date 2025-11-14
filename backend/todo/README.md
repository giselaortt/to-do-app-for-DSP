# Django REST Framework Todo Backend

Backend API for a To-Do list application built with Django and Django REST Framework.

## Setup Instructions

### 1. Navigate to the project directory
```bash
cd backend/todo
```

### 2. Create and activate a virtual environment

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create database migrations
```bash
python manage.py makemigrations
```

### 5. Apply migrations to create the database
```bash
python manage.py migrate
```

### 6. (Optional) Create a superuser for Django admin
```bash
python manage.py createsuperuser
```

## Running the Server

Start the development server:
```bash
python manage.py runserver
```

The server will run on `http://127.0.0.1:8000/`

## API Endpoints

All endpoints are available at `/api/todos/`:

- `GET /api/todos/` - List all tasks
- `POST /api/todos/` - Create a new task
- `GET /api/todos/{id}/` - Get a specific task by ID
- `PUT /api/todos/{id}/` - Update a task (full update)
- `PATCH /api/todos/{id}/` - Update a task (partial update)
- `DELETE /api/todos/{id}/` - Delete a task

### Example API Usage

**Create a task:**
```bash
curl -X POST http://127.0.0.1:8000/api/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "description": "Task description", "status": "open"}'
```

**List all tasks:**
```bash
curl http://127.0.0.1:8000/api/todos/
```

**Update a task:**
```bash
curl -X PUT http://127.0.0.1:8000/api/todos/1/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "description": "Updated description", "status": "in_progress"}'
```

**Delete a task:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/todos/1/
```

## Task Model

- `id`: Auto-incremental unique identifier (primary key)
- `title`: Required field (max 200 characters)
- `description`: Optional field
- `status`: Enum with choices: `open`, `in_progress`, `done` (default: `open`)
- `created_at`: Timestamp when task was created (auto-generated)
- `updated_at`: Timestamp when task was last updated (auto-generated)

## Running Tests

Run all tests:
```bash
python manage.py test
```

Run tests for the tasks app only:
```bash
python manage.py test tasks
```

## Django Admin

Access the Django admin interface at:
```
http://127.0.0.1:8000/admin/
```

Use the superuser credentials created in step 6 to log in.

## Database

The application uses SQLite by default. The database file (`db.sqlite3`) will be created automatically in the `backend/todo/` directory after running migrations.

