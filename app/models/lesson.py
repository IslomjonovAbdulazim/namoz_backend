from datetime import datetime
from pydantic import BaseModel


class Lesson(BaseModel):
    id: str
    title: str
    description: str
    video_url: str
    pdf_url: str
    ppt_url: str
    is_published: bool = True
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }