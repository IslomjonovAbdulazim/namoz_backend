# Student Authentication API

## Web/Mobile Authentication Flow

### Request OTP Code
**POST /auth/request-otp**
```json
Request:
{
  "phone_number": "+998901234567"
}

Response:
{
  "message": "OTP code will be sent via Telegram bot",
  "phone_number": "+998901234567",
  "code_id": "uuid",
  "expires_in": 300
}
```

### Verify OTP Code
**POST /auth/verify-otp**
```json
Request:
{
  "phone_number": "+998901234567",
  "otp_code": "123456"
}

Response (if user exists):
{
  "access_token": "jwt_token",
  "user": {
    "id": "uuid",
    "full_name": "string",
    "telegram_id": 123456789,
    "phone_number": "+998901234567",
    "joined_at": "2024-01-01T00:00:00Z"
  }
}

Response (if user not found):
{
  "error": "user_not_found",
  "message": "Please register via Telegram bot first",
  "phone_number": "+998901234567"
}
```

## Telegram Bot Authentication

### Bot Login Command
**POST /bot/login**
```json
Request:
{
  "telegram_id": 123456789
}

Response (if pending OTP exists):
{
  "action": "send_otp",
  "otp_code": "123456",
  "phone_number": "+998901234567",
  "message": "Here is your login code: 123456"
}

Response (if no pending OTP):
{
  "action": "no_otp",
  "message": "No pending login requests found"
}
```

## Registration
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

## Login
**POST /auth/login**
```json
Request:
{
  "telegram_id": 123456789
}

        
Response (if phone number exists):
{
  "access_token": "jwt_token",
  "user": {
    "id": "uuid",
    "full_name": "string",
    "telegram_id": 123456789,
    "phone_number": "+998901234567",
    "joined_at": "2024-01-01T00:00:00Z"
  }
}

Response (if phone number missing):
{
  "error": "phone_number_required",
  "message": "Phone number is required to continue",
  "user_id": "uuid",
  "telegram_id": 123456789
}
```