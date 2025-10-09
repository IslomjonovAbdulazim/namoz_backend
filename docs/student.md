# Student API Endpoints

## Authentication
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

## Profile Management
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

## Lessons
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

## Lesson Access
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

**GET /access/lessons/{lesson_id}**
```json
Response:
{
  "has_access": true,
  "access_details": {
    "is_unlocked": true,
    "unlocked_at": "2024-01-01T00:00:00Z",
    "amount": 50000,
    "paid_at": "2024-01-01T00:00:00Z"
  }
}
```

## Tests
**GET /lessons/{lesson_id}/questions**
```json
Response:
[
  {
    "id": "uuid",
    "lesson_id": "uuid",
    "question_text": "string",
    "options": ["option1", "option2", "option3", "option4"]
  }
]
```

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

## Test Results
**GET /results**
```json
Response:
[
  {
    "id": "uuid",
    "lesson_id": "uuid",
    "lesson_title": "string",
    "score": 85,
    "total_questions": 10,
    "started_at": "2024-01-01T00:00:00Z",
    "ended_at": "2024-01-01T00:00:00Z"
  }
]
```

**GET /results/{result_id}**
```json
Response:
{
  "id": "uuid",
  "user_id": "uuid",
  "lesson_id": "uuid",
  "lesson_title": "string",
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