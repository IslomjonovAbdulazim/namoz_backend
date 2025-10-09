# Namoz Backend Development Plan

## Project Overview
FastAPI-based backend for Namoz education platform with PostgreSQL database, Redis caching, and comprehensive user/lesson management.

## Development Roadmap

### High Priority Tasks
1. **Database Configuration & Connection**
   - Set up SQLAlchemy models and PostgreSQL connection
   - Configure database migrations
   - Establish connection pooling

2. **User Management API**
   - User registration and authentication endpoints
   - Profile management (CRUD operations)
   - User session handling

3. **Lesson Management API**
   - Create, read, update lesson content
   - Progress tracking and completion status
   - Lesson categorization and filtering

4. **Authentication & Authorization**
   - JWT token implementation
   - Role-based access control
   - Middleware for protected routes

### Medium Priority Tasks
5. **Testing System**
   - Question management endpoints
   - Test result tracking and analytics
   - Scoring and evaluation logic

6. **Redis Caching Layer**
   - Session management
   - Performance optimization for frequent queries
   - Cache invalidation strategies

7. **Input Validation & Error Handling**
   - Comprehensive request validation
   - Standardized error responses
   - Logging and monitoring

### Low Priority Tasks
8. **API Documentation**
   - Enhanced OpenAPI schemas
   - Request/response examples
   - Integration guides

## Current Project Structure
```
app/
├── api/          # API route handlers
├── core/         # Core configuration and utilities
├── models/       # Pydantic models (User, Lesson, TestQuestion, TestResult, Access)
├── services/     # Business logic services
└── utils/        # Helper functions

docs/             # Documentation
main.py           # FastAPI application entry point
requirements.txt  # Dependencies
```

## Technology Stack
- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLAlchemy 2.0.23
- **Caching**: Redis 5.0.1
- **Server**: Uvicorn 0.24.0
- **Validation**: Pydantic 2.5.0

## API Endpoints

### Authentication
**POST /auth/register**
```json
Request:
{
  "full_name": "string",
  "telegram_id": 123456789,
  "phone_number": "+998901234567"
}

Response:
{
  "id": "uuid",
  "full_name": "string",
  "telegram_id": 123456789,
  "phone_number": "+998901234567",
  "joined_at": "2024-01-01T00:00:00Z",
  "access_token": "jwt_token"
}
```

**POST /auth/login**
```json
Request:
{
  "telegram_id": 123456789
}

Response:
{
  "access_token": "jwt_token",
  "user": {
    "id": "uuid",
    "full_name": "string",
    "telegram_id": 123456789,
    "phone_number": "+998901234567"
  }
}
```

### User Management
**GET /users/profile**
```json
Response:
{
  "id": "uuid",
  "full_name": "string",
  "telegram_id": 123456789,
  "phone_number": "+998901234567",
  "joined_at": "2024-01-01T00:00:00Z"
}
```

**PUT /users/profile**
```json
Request:
{
  "full_name": "string",
  "phone_number": "+998901234567"
}

Response:
{
  "id": "uuid",
  "full_name": "string",
  "telegram_id": 123456789,
  "phone_number": "+998901234567",
  "joined_at": "2024-01-01T00:00:00Z"
}
```

### Lesson Management
**GET /lessons**
```json
Response:
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "video_url": "string",
    "pdf_url": "string",
    "ppt_url": "string",
    "is_published": true,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

**GET /lessons/{lesson_id}**
```json
Response:
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "video_url": "string",
  "pdf_url": "string",
  "ppt_url": "string",
  "is_published": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Lesson Access
**GET /access/lessons**
```json
Response:
[
  {
    "lesson": {
      "id": "uuid",
      "title": "string",
      "description": "string"
    },
    "access": {
      "is_unlocked": true,
      "unlocked_at": "2024-01-01T00:00:00Z"
    }
  }
]
```

**POST /access/lessons/{lesson_id}**
```json
Request:
{
  "amount": 50000
}

Response:
{
  "id": "uuid",
  "user_id": "uuid",
  "lesson_id": "uuid",
  "is_unlocked": true,
  "unlocked_at": "2024-01-01T00:00:00Z",
  "amount": 50000,
  "paid_at": "2024-01-01T00:00:00Z"
}
```

### Test Questions
**GET /lessons/{lesson_id}/questions**
```json
Response:
[
  {
    "id": "uuid",
    "lesson_id": "uuid",
    "question_text": "string",
    "options": ["option1", "option2", "option3", "option4"],
    "correct_option": 0
  }
]
```

### Test Results
**POST /lessons/{lesson_id}/test**
```json
Request:
{
  "answers": [
    {
      "question_id": "uuid",
      "selected_option": 0
    }
  ]
}

Response:
{
  "id": "uuid",
  "user_id": "uuid",
  "lesson_id": "uuid",
  "score": 85,
  "total_questions": 10,
  "answers": [
    {
      "question": "string",
      "user_selected": "string",
      "correct": "string"
    }
  ],
  "started_at": "2024-01-01T00:00:00Z",
  "ended_at": "2024-01-01T00:00:00Z"
}
```

**GET /results**
```json
Response:
[
  {
    "id": "uuid",
    "lesson_id": "uuid",
    "score": 85,
    "total_questions": 10,
    "started_at": "2024-01-01T00:00:00Z",
    "ended_at": "2024-01-01T00:00:00Z"
  }
]
```

### Health & Status
**GET /**
```json
Response:
{
  "message": "Namoz Education API",
  "status": "running"
}
```

**GET /health**
```json
Response:
{
  "status": "healthy",
  "models_loaded": true
}
```

## Next Steps
Ready to begin implementation starting with database configuration and core API endpoints.