from datetime import datetime
from typing import List
from pydantic import BaseModel


class UserAnswer(BaseModel):
    question: str
    user_selected: str
    correct: str


class UserTestResult(BaseModel):
    id: str
    user_id: str
    lesson_id: str
    score: int
    total_questions: int
    answers: List[UserAnswer]
    started_at: datetime
    ended_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }