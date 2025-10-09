# Admin API Endpoints

## Authentication
**POST /admin/auth/login**
```json
Request:
{
  "email": "admin@gmail.com",
  "password": "admin123"
}

Response:
{
  "access_token": "jwt_admin_token",
  "token_type": "bearer",
  "expires_in": 3600
}
```

*Note: All admin endpoints require Bearer token authentication in the Authorization header.*

## User Management
**GET /admin/users** 
*Headers: Authorization: Bearer {admin_token}*
```json
Response:
[
  {
    "id": "uuid",
    "full_name": "string",
    "telegram_id": 123456789,
    "phone_number": "+998901234567",
    "joined_at": "2024-01-01T00:00:00Z",
    "total_lessons_purchased": 5,
    "total_spent": 250000
  }
]
```

**GET /admin/users/{user_id}**
*Headers: Authorization: Bearer {admin_token}*
```json
Response:
{
  "id": "uuid",
  "full_name": "string",
  "telegram_id": 123456789,
  "phone_number": "+998901234567",
  "joined_at": "2024-01-01T00:00:00Z",
  "lessons_purchased": [
    {
      "lesson_id": "uuid",
      "lesson_title": "string",
      "amount": 50000,
      "paid_at": "2024-01-01T00:00:00Z"
    }
  ],
  "test_results": [
    {
      "lesson_id": "uuid",
      "lesson_title": "string",
      "score": 85,
      "total_questions": 10,
      "completed_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

**DELETE /admin/users/{user_id}**
*Headers: Authorization: Bearer {admin_token}*
```json
Response:
{
  "message": "User deleted successfully"
}
```

## Lesson Management
**GET /admin/lessons**
*Headers: Authorization: Bearer {admin_token}*
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
    "created_at": "2024-01-01T00:00:00Z",
    "total_users": 150,
    "total_revenue": 7500000,
    "average_score": 78.5
  }
]
```

**POST /admin/lessons**
*Headers: Authorization: Bearer {admin_token}*
```json
Request:
{
  "title": "string",
  "description": "string",
  "video_url": "string",
  "pdf_url": "string",
  "ppt_url": "string",
  "is_published": false
}

Response:
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "video_url": "string",
  "pdf_url": "string",
  "ppt_url": "string",
  "is_published": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

**PUT /admin/lessons/{lesson_id}**
*Headers: Authorization: Bearer {admin_token}*
```json
Request:
{
  "title": "string",
  "description": "string",
  "video_url": "string",
  "pdf_url": "string",
  "ppt_url": "string"
}

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

**DELETE /admin/lessons/{lesson_id}**
*Headers: Authorization: Bearer {admin_token}*
```json
Response:
{
  "message": "Lesson deleted successfully"
}
```

**PUT /admin/lessons/{lesson_id}/publish**
*Headers: Authorization: Bearer {admin_token}*
```json
Request:
{
  "is_published": true
}

Response:
{
  "id": "uuid",
  "title": "string",
  "is_published": true,
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## Question Management
**GET /admin/lessons/{lesson_id}/questions**
*Headers: Authorization: Bearer {admin_token}*
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

**POST /admin/lessons/{lesson_id}/questions**
*Headers: Authorization: Bearer {admin_token}*
```json
Request:
{
  "question_text": "string",
  "options": ["option1", "option2", "option3", "option4"],
  "correct_option": 0
}

Response:
{
  "id": "uuid",
  "lesson_id": "uuid",
  "question_text": "string",
  "options": ["option1", "option2", "option3", "option4"],
  "correct_option": 0
}
```

**PUT /admin/questions/{question_id}**
*Headers: Authorization: Bearer {admin_token}*
```json
Request:
{
  "question_text": "string",
  "options": ["option1", "option2", "option3", "option4"],
  "correct_option": 0
}

Response:
{
  "id": "uuid",
  "lesson_id": "uuid",
  "question_text": "string",
  "options": ["option1", "option2", "option3", "option4"],
  "correct_option": 0
}
```

**DELETE /admin/questions/{question_id}**
*Headers: Authorization: Bearer {admin_token}*
```json
Response:
{
  "message": "Question deleted successfully"
}
```

## Analytics & Reports
**GET /admin/lessons/{lesson_id}/analytics**
*Headers: Authorization: Bearer {admin_token}*
```json
Response:
{
  "lesson_id": "uuid",
  "lesson_title": "string",
  "total_students": 150,
  "total_revenue": 7500000,
  "average_score": 78.5,
  "completion_rate": 85.2,
  "recent_purchases": [
    {
      "user_id": "uuid",
      "user_name": "string",
      "amount": 50000,
      "paid_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

**GET /admin/lessons/{lesson_id}/results**
*Headers: Authorization: Bearer {admin_token}*
```json
Response:
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "user_name": "string",
    "score": 85,
    "total_questions": 10,
    "completion_time": "00:15:30",
    "started_at": "2024-01-01T00:00:00Z",
    "ended_at": "2024-01-01T00:00:00Z"
  }
]
```

**GET /admin/dashboard**
*Headers: Authorization: Bearer {admin_token}*
```json
Response:
{
  "total_users": 1250,
  "total_lessons": 25,
  "total_revenue": 62500000,
  "monthly_revenue": 12500000,
  "new_users_this_month": 150,
  "most_popular_lessons": [
    {
      "lesson_id": "uuid",
      "title": "string",
      "student_count": 350,
      "revenue": 17500000
    }
  ],
  "recent_activity": [
    {
      "type": "purchase",
      "user_name": "string",
      "lesson_title": "string",
      "amount": 50000,
      "timestamp": "2024-01-01T00:00:00Z"
    },
    {
      "type": "test_completion",
      "user_name": "string",
      "lesson_title": "string",
      "score": 85,
      "timestamp": "2024-01-01T00:00:00Z"
    }
  ]
}
```

## Access Management
**GET /admin/access/all**
*Headers: Authorization: Bearer {admin_token}*
```json
Response:
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "user_name": "string",
    "lesson_id": "uuid",
    "lesson_title": "string",
    "amount": 50000,
    "paid_at": "2024-01-01T00:00:00Z",
    "notes": "string"
  }
]
```

**POST /admin/access/grant**
*Headers: Authorization: Bearer {admin_token}*
```json
Request:
{
  "user_id": "uuid",
  "lesson_id": "uuid",
  "amount": 0,
  "notes": "Admin granted access"
}

Response:
{
  "id": "uuid",
  "user_id": "uuid",
  "lesson_id": "uuid",
  "is_unlocked": true,
  "unlocked_at": "2024-01-01T00:00:00Z",
  "amount": 0,
  "paid_at": "2024-01-01T00:00:00Z",
  "notes": "Admin granted access"
}
```