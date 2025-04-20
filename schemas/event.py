from pydantic import BaseModel
from typing import Optional

class EventSchema(BaseModel):
    id: int
    subject: str
    body: Optional[str]
    start: datetime
    end: Optional[datetime]
    user_id: