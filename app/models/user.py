from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: str
    full_name: str
    telegram_id: int
    phone_number: str
    joined_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }