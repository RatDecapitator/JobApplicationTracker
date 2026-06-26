# Job Application Tracker

Simple REST API built with FastAPI for tracking job applications.

## Features

- Create job applications
- View all applications
- Update application status
- Delete applications
- Save recruiter responses
- View application statistics
- Interactive Swagger documentation
- API tests with Pytest

## Technologies

- Python
- FastAPI
- SQLite
- Pydantic
- Pytest

## Installation

```bash
git clone <repository-url>
cd JobApplicationTracker
pip install -r requirements.txt
```

## Run

```bash
uvicorn src.api:app --reload
```

Swagger:

```
http://127.0.0.1:8000/docs
```

## Run tests

```bash
PYTHONPATH=. pytest -v
```

## Available endpoints

| Method | Endpoint |
|---------|----------|
| GET | /applications |
| GET | /applications/{id} |
| POST | /applications |
| PATCH | /applications/{id}/status |
| DELETE | /applications/{id} |
| POST | /applications/{id}/responses |
| GET | /applications/{id}/responses |
| GET | /statistics |

## Future improvements

- Authentication
- PostgreSQL
- SQLAlchemy
- Docker

## What I learned

This project helped me practice:

- REST API design
- FastAPI
- SQLite
- CRUD operations
- Pydantic models
- API testing with Pytest
- Basic backend architecture