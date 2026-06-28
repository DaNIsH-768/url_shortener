# Shortly

As a graduate student, I often found myself juggling too many links: research papers, lecture notes, GitHub repositories, and random references that I needed to share quickly. I wanted a small personal tool that could turn long URLs into something cleaner, faster, and easier to remember without making the whole thing feel overly complicated.

That is how this project began: a simple URL shortener API built with FastAPI, SQLModel, PostgreSQL, Redis, and JWT-based authentication. It is not just a toy project for me; it is a practical little service that reflects the kind of software I enjoy building while learning, experimenting, and improving my backend skills.

## Why I built it

This project helped me explore a few things that matter to me as a developer:

- building a real API with authentication and protected routes
- working with relational data and persistence in PostgreSQL
- adding caching and rate limiting for a more robust experience
- practicing clean backend design while keeping the project lightweight

## What it does

Shortly lets users:

- create an account and log in securely
- shorten long URLs into compact short links
- view the links they have created
- redirect through a short code to the original destination
- benefit from basic rate limiting and Redis-backed caching

## Tech stack

- Python 3.12+
- FastAPI for the API layer
- SQLModel for database models
- PostgreSQL for persistent storage
- Redis for quick URL lookups and caching
- JWT for authentication
- Pytest for automated tests

## Project structure

- app/main.py: app entry point and router registration
- app/routers/auth.py: registration and login endpoints
- app/routers/urls.py: URL creation, listing, and redirection logic
- app/models.py: SQLModel definitions for users, URLs, and clicks
- app/database.py: database and Redis setup
- tests/: API tests covering auth and URL behavior

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/url_shortener.git
cd url_shortener
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a .env file with values similar to:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/urlshortener
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://localhost:6379
```

Make sure PostgreSQL and Redis are running locally before starting the app.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

The API should now be available at:

```text
http://127.0.0.1:8000
```

## Live API

You can explore the deployed API documentation here:

- https://urlshortener-production-0dc0.up.railway.app/docs

## API overview

### Authentication

- POST /auth/register: create a new account
- POST /auth/login: log in and receive a JWT token

### URL management

- POST /urls: shorten a URL
- GET /urls: list URLs created by the authenticated user
- GET /{short_code}: redirect to the original URL
- GET /health: health check endpoint

### Example usage

> Note: after logging in, copy the JWT token returned by the login endpoint and paste it into the Authorize button in the API docs. If the token appears with quotation marks around it, remove the quotes before submitting.

Register a user:

```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"securepass123","confirm_password":"securepass123"}'
```

Log in:

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"securepass123"}'
```

Create a shortened URL:

```bash
curl -X POST "http://127.0.0.1:8000/urls" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

## Testing

Run the test suite with:

```bash
pytest
```

## A note from the developer

I built this project as a way to turn an everyday problem into something concrete and useful. It is simple, but it taught me a lot about backend architecture, API design, data modeling, and the small decisions that make a service feel reliable.

If you want to improve it further, I would love to see features like custom short links, analytics dashboards, expiration dates, and better error handling.
