from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserLessonAccess(BaseModel):
    id: str
    user_id: str
    lesson_id: str
    is_unlocked: bool = True
    unlocked_at: datetime
    amount: int
    paid_at: datetime
    notes: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }