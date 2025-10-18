# Student Bot API Endpoints

*Note: Bot endpoints use telegram_id for authentication - no Bearer tokens required.*

## Lessons & Access
**GET /bot/user/{telegram_id}/lessons**
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

**GET /bot/user/{telegram_id}/lesson/{lesson_id}**
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

## Test Management
**GET /bot/user/{telegram_id}/lesson/{lesson_id}/questions**
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

**POST /bot/user/{telegram_id}/lesson/{lesson_id}/test**
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
**GET /bot/user/{telegram_id}/results**
```json
Response:
[
  {
    "id": "uuid",
    "lesson_id": "uuid",
    "lesson_title": "string",
    "score": 85,
    "total_questions": 10,
    "completed_at": "2024-01-01T00:00:00Z"
  }
]
```

**GET /bot/user/{telegram_id}/result/{result_id}**
```json
Response:
{
  "id": "uuid",
  "lesson_title": "string",
  "score": 85,
  "total_questions": 10,
  "answers": [
    {
      "question": "string",
      "user_selected": "string",
      "correct": "string",
      "is_correct": false
    }
  ],
  "completed_at": "2024-01-01T00:00:00Z"
}
```