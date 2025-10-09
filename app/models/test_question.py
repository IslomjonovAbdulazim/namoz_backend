from typing import List
from pydantic import BaseModel


class TestQuestion(BaseModel):
    id: str
    lesson_id: str
    question_text: str
    options: List[str]
    correct_option: int