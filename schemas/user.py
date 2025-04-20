from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    id: str #microsoft id
    email: str
    name: str | None = None
    
    class Config:
        orm_mode = True