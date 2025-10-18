# Student Web/Mobile API Endpoints

*Note: All endpoints require Bearer token authentication in Authorization header.*

## Profile Management
**GET /users/profile**
*Headers: Authorization: Bearer {token}*
```json
Response:
{
  "id": "uuid",
  "full_name": "string",
  "telegram_id": 123456789,
  "phone_number": "+998901234567"
  "joined_at": "2024-01-01T00:00:00Z"
}
```

**PUT /users/profile**
*Headers: Authorization: Bearer {token}*
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
*Headers: Authorization: Bearer {token}*
```json
Response:
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "has_access": true,
    "test_completed": false,
    "score": null,
    "price": 50000
  }
]
```

**GET /lessons/{lesson_id}**
*Headers: Authorization: Bearer {token}*
```json
Response:
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "video_url": "string",
  "pdf_url": "string",
  "ppt_url": "string",
  "has_access": true,
  "test_completed": false,
  "score": null
}
```

## Lesson Access
**GET /access/lessons**
*Headers: Authorization: Bearer {token}*
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

**GET /access/lessons/{lesson_id}**
*Headers: Authorization: Bearer {token}*
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
*Headers: Authorization: Bearer {token}*
```json
Response:
[
  {
    "id": "uuid",
    "question_text": "string",
    "options": ["option1", "option2", "option3", "option4"]
  }
]
```

**POST /lessons/{lesson_id}/test**
*Headers: Authorization: Bearer {token}*
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
  "score": 85,
  "total_questions": 10,
  "passed": true,
  "message": "Congratulations! You scored 85%"
}
```

## Test Results
**GET /results**
*Headers: Authorization: Bearer {token}*
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
*Headers: Authorization: Bearer {token}*
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