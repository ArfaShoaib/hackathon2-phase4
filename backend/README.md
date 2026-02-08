---
title: FastAPI Backend
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---



# Todo Backend API

A complete, production-ready, secure Python FastAPI backend for a multi-user Todo application. The backend provides user registration with secure password hashing, JWT token verification for Better Auth frontend integration, and comprehensive task CRUD operations with strict ownership enforcement.

## Prerequisites

- Python 3.12+
- uv (Python package manager)
- PostgreSQL database (or compatible database)

## Installation

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies:
   ```bash
   cd backend
   uv sync
   ```

## Environment Setup

Create a `.env` file in the backend directory with the following variables:

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
JWKS_URL=https://your-better-auth-domain/api/auth/jwks
JWT_ISSUER=your-issuer
JWT_AUDIENCE=your-audience
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### OpenAI Domain Allowlist Setup

To use the AI chatbot functionality, you need to register your domain with OpenAI:

1. Visit the OpenAI platform and navigate to your project settings
2. Add your domain to the allowed domains list
3. Generate a domain key for your specific backend deployment
4. Add the domain key to your frontend environment variables as `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`

## Running the Application

### Development

```bash
cd backend
source .venv/Scripts/activate  # On Windows
# source .venv/bin/activate  # On Linux/Mac
uv run python main.py
```

### Or using uvicorn directly

```bash
cd backend
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication

- `POST /api/auth/signup` - Register a new user

### AI Chatbot

- `POST /api/{user_id}/chat` - Interact with the AI chatbot to manage tasks via natural language
  - Headers: `Authorization: Bearer {jwt_token}`
  - Request body: `{"conversation_id": 123, "message": "Add task: Buy groceries"}`
  - Response: `{"conversation_id": 123, "response": "Task 'Buy groceries' has been created successfully.", "tool_calls": []}`

### Task Management

- `GET /api/{user_id}/tasks` - Get all tasks for a user

Request body:
```json
{
  "email": "user@example.com",
  "password": "secure_password_123"
}
```

Response:
- 201: User created successfully
- 400: Invalid email format or password strength
- 409: Email already exists

### Task Management

All task endpoints require authentication via JWT token in Authorization header.

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task completely
- `PATCH /api/{user_id}/tasks/{task_id}` - Update a task partially
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Update task completion status
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task

## CORS Configuration

The backend is configured to allow requests from the following origins:

- Local development: `http://localhost:3000`, `http://localhost:3001`, `http://127.0.0.1:3000`, `http://127.0.0.1:3001`
- Production frontend: `https://hackathon2-phase3-chatbot.vercel.app`
- Production backend: `https://arfa000-hackathon2-phase3-aichatbot.hf.space`

If you need to add additional origins, modify the `allow_origins` list in `main.py`.

## Security Features

- Passwords are securely hashed using bcrypt with 12 rounds
- JWT token verification using Better Auth JWKS
- Strict ownership enforcement - users can only access their own tasks
- Input validation on all endpoints
- Protection against common vulnerabilities

## Health Check

- `GET /` - Health check endpoint
- `GET /health` - Alternative health check endpoint

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success for GET requests
- 201: Created for POST requests
- 204: No Content for DELETE requests
- 400: Bad Request for validation errors
- 401: Unauthorized for authentication failures
- 403: Forbidden for authorization failures
- 404: Not Found for missing resources
- 409: Conflict for duplicate resources
- 422: Unprocessable Entity for validation errors
- 500: Internal Server Error for unexpected errors

## Smoke Test Checklist

- [ ] Server starts without errors
- [ ] Health check endpoints return healthy status
- [ ] User can register with valid email and password
- [ ] Duplicate email registration returns 409 Conflict
- [ ] Invalid email format returns 400 Bad Request
- [ ] Weak password returns 400 Bad Request
- [ ] Authenticated user can create a task
- [ ] Authenticated user can retrieve their tasks
- [ ] User cannot access another user's tasks
- [ ] Authenticated user can update their task
- [ ] Authenticated user can delete their task
- [ ] JWT token verification works correctly
- [ ] All endpoints return appropriate error codes
- [ ] Database operations complete successfully
