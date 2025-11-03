# Telegram Bot API Documentation

## Overview
This document describes all API endpoints used by the Telegram bot for the Namoz Education platform. The bot provides students with access to lessons, tests, and progress tracking.

## Base URL
```
https://api.nomoz.uz/bot
```

## Authentication
All endpoints use the Telegram user ID for authentication and authorization.

---

## 📚 User Management

### Register User
Register a new user from Telegram bot.

**Endpoint:** `POST /register`

**Request Body:**
```json
{
  "telegram_id": 1038753516,
  "full_name": "Abduazim Doe", 
  "phone_number": "+998901234567"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user_id": "uuid-string",
  "telegram_id": 1038753516
}
```

---

## 📖 Lessons

### Get User Lessons
Get all lessons available to a user with access information.

**Endpoint:** `GET /user/{telegram_id}/lessons`

**Parameters:**
- `telegram_id` (int): User's Telegram ID

**Response:**
```json
[
  {
    "id": "1cd67e6f-c024-44ea-b259-a94a1e3d4211",
    "title": "1-Dars",
    "description": "Fonetika asoslari",
    "price": 50000,
    "has_access": true,
    "score": 85,
    "test_completed": true
  },
  {
    "id": "2cd67e6f-c024-44ea-b259-a94a1e3d4212", 
    "title": "2-Dars",
    "description": "Morfologiya",
    "price": 75000,
    "has_access": false,
    "score": null,
    "test_completed": false
  }
]
```

### Get Lesson Details
Get detailed information about a specific lesson.

**Endpoint:** `GET /user/{telegram_id}/lesson/{lesson_id}`

**Parameters:**
- `telegram_id` (int): User's Telegram ID
- `lesson_id` (string): UUID of the lesson

**Response:**
```json
{
  "id": "1cd67e6f-c024-44ea-b259-a94a1e3d4211",
  "title": "1-Dars",
  "description": "Fonetika asoslari haqida batafsil ma'lumot",
  "content": "Lesson content here...",
  "video_url": "https://example.com/video.mp4",
  "pdf_url": "https://example.com/lesson.pdf", 
  "presentation_url": "https://example.com/slides.ppt",
  "price": 50000,
  "has_access": true,
  "test_completed": true,
  "score": 85
}
```

---

## ❓ Tests & Questions

### Get Lesson Questions
Get test questions for a specific lesson.

**Endpoint:** `GET /user/{telegram_id}/lesson/{lesson_id}/questions`

**Parameters:**
- `telegram_id` (int): User's Telegram ID  
- `lesson_id` (string): UUID of the lesson

**Response:**
```json
[
  {
    "id": "21af109a-0c56-4bbb-9a4d-374dc165d7e6",
    "question_text": "Monografiya so'zida urg'u qaysi bo'g'inga tushgan?",
    "options": [
      "3-bo'g'in",
      "1-bo'g'in", 
      "2-bo'g'in",
      "4-bo'g'in"
    ]
  },
  {
    "id": "31af109a-0c56-4bbb-9a4d-374dc165d7e7",
    "question_text": "Quyida berilgan baytda nechta so'zda ochiq bo'g'in mavjud?\nIlmdan bir shu'la dilga tushgan on,\nAniq bilursankim, ilm bepoyon.",
    "options": [
      "4 ta",
      "5 ta",
      "6 ta", 
      "7 ta"
    ]
  }
]
```

### Submit Test Answers
Submit test answers and get results.

**Endpoint:** `POST /user/{telegram_id}/lesson/{lesson_id}/test`

**Parameters:**
- `telegram_id` (int): User's Telegram ID
- `lesson_id` (string): UUID of the lesson

**Request Body:**
```json
{
  "answers": [
    {
      "question_id": "21af109a-0c56-4bbb-9a4d-374dc165d7e6",
      "selected_option": 0
    },
    {
      "question_id": "31af109a-0c56-4bbb-9a4d-374dc165d7e7", 
      "selected_option": 2
    }
  ]
}
```

**Response:**
```json
{
  "score": 80,
  "correct_answers": 12,
  "total_questions": 15,
  "passed": true,
  "result_id": "41af109a-0c56-4bbb-9a4d-374dc165d7e8"
}
```

---

## 📊 Results & Progress

### Get User Results
Get user's test results history.

**Endpoint:** `GET /user/{telegram_id}/results`

**Parameters:**
- `telegram_id` (int): User's Telegram ID
- `limit` (int, optional): Limit number of results

**Response:**
```json
[
  {
    "id": "41af109a-0c56-4bbb-9a4d-374dc165d7e8",
    "lesson_title": "1-Dars",
    "score": 80,
    "correct_answers": 12,
    "total_questions": 15,
    "passed": true,
    "completed_at": "2025-11-01T07:30:00Z"
  }
]
```

### Get Result Details
Get detailed information about a specific test result.

**Endpoint:** `GET /bot/user/{telegram_id}/result/{result_id}`

**Parameters:**
- `telegram_id` (int): User's Telegram ID
- `result_id` (int): ID of the test result

**Response:**
```json
{
    "lesson_title": "1-Dars",
    "score": 80,
    "correct_answers": 12,
    "total_questions": 15,
    "completed_at": "2025-11-01T07:30:00Z",
    "answers": [
      {
        "question_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "question_text": "O'zbek tilida nechta unli harf bor?",
        "options": ["4 ta", "5 ta", "6 ta", "7 ta"],
        "selected_option": 2,
        "correct_option": 2,
        "is_correct": true
      },
      {
        "question_id": "b2c3d4e5-f6g7-8901-bcde-f12345678901",
        "question_text": "Fonetika nima?",
        "options": ["Tovush tizimi", "So'z yasalishi", "Gap tuzilishi", "Ma'no o'rganish"],
        "selected_option": 0,
        "correct_option": 0,
        "is_correct": true
      },
      {
        "question_id": "c3d4e5f6-g7h8-9012-cdef-123456789012",
        "question_text": "Undosh tovushlar nechta?",
        "options": ["20 ta", "21 ta", "22 ta", "23 ta"],
        "selected_option": 1,
        "correct_option": 2,
        "is_correct": false
      }
    ]
  }

```

### Get User Statistics
Get user's overall statistics.

**Endpoint:** `GET /user/{telegram_id}/stats`

**Parameters:**
- `telegram_id` (int): User's Telegram ID

**Response:**
```json
{
  "phone": "+998901234567",
  "total_tests": 5,
  "passed_tests": 4,
  "average_score": 78.5,
  "registration_date": "01.10.2025"
}
```

### Get User Progress
Get user's learning progress overview.

**Endpoint:** `GET /user/{telegram_id}/progress`

**Parameters:**
- `telegram_id` (int): User's Telegram ID

**Response:**
```json
{
  "total_lessons": 10,
  "accessible_lessons": 5,
  "completed_lessons": 3,
  "total_tests": 5,
  "passed_tests": 4,
  "average_score": 78.5,
  "last_test_date": "01.11.2025",
  "last_login": "Bugun"
}
```

---

## 🔄 Bot Workflow

### 1. User Registration Flow
```
1. User starts bot → /start command
2. Bot requests phone number
3. User shares contact
4. Bot calls POST /register
5. User is registered and can access bot features
```

### 2. Lesson Access Flow
```
1. User clicks "My Lessons" → GET /user/{id}/lessons
2. User selects lesson → GET /user/{id}/lesson/{lesson_id}
3. If has_access = true: Show materials and test button
4. If has_access = false: Show purchase button with admin contact
```

### 3. Test Taking Flow
```
1. User clicks "Take Test" → GET /user/{id}/lesson/{lesson_id}/questions
2. Bot shows questions one by one with A/B/C/D buttons
3. User answers all questions
4. Bot submits answers → POST /user/{id}/lesson/{lesson_id}/test
5. Bot shows test results
```

### 4. Results Viewing Flow
```
1. User clicks "My Results" → GET /user/{id}/results
2. User can view detailed result → GET /user/{id}/result/{result_id}
3. User can view progress → GET /user/{id}/progress
4. User can view profile → GET /user/{id}/stats
```

---

## 🎯 Key Features

### Multi-line Support
- **Questions** can contain multiple paragraphs, poetry, code examples
- **Options** can be lengthy explanations
- **No character limits** for question/option text

### Smart Button Layout
- **Question text and options** displayed in message (unlimited length)
- **Answer buttons** show only "A", "B", "C", "D" (never truncate)
- **2x2 grid layout** for clean appearance

### Admin Contact Integration
- **Locked lessons** include smart contact links
- **Pre-filled messages** with user name and lesson details
- **Easy admin workflow** with copyable user names in backticks

### Test Retaking
- Users can **retake tests unlimited times**
- Always shows "Test topshirish" button
- No restrictions on test attempts

---

## 🛠️ Error Handling

### Common Error Responses
- `400 Bad Request`: Invalid lesson ID format
- `403 Forbidden`: Access denied (no lesson access)
- `404 Not Found`: User/lesson/result not found
- `500 Internal Server Error`: Server error

### Error Response Format
```json
{
  "detail": "Error message description"
}
```

---

## 📋 Data Models

### User Registration
```json
{
  "telegram_id": "integer",
  "full_name": "string", 
  "phone_number": "string"
}
```

### Test Answer
```json
{
  "question_id": "string (UUID)",
  "selected_option": "integer (0-3)"
}
```

### Test Submission
```json
{
  "answers": ["array of TestAnswer objects"]
}
```

---

## 🔧 Implementation Notes

1. **UUID Support**: All lesson and question IDs are UUIDs (strings)
2. **Telegram ID**: Used as primary user identifier
3. **Phone Format**: Stored with country code (+998...)
4. **Date Format**: ISO 8601 format for API, dd.mm.yyyy for display
5. **Score Calculation**: Percentage (0-100), 70%+ considered passing
6. **Caching**: Bot implements intelligent caching for better performance

---

## 🏗️ Architecture

```
Telegram Bot ↔ FastAPI Backend ↔ PostgreSQL Database
     ↑              ↑                    ↑
User Interface   Business Logic     Data Storage
```

The bot serves as the user interface, the FastAPI backend handles business logic and data processing, and PostgreSQL stores all user data, lessons, questions, and results.