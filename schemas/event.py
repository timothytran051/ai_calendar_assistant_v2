from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class event_create_schema(BaseModel): #the client defines the information, containing data that is needed to create the event aka user input
    subject: str
    body: Optional[str]
    start: datetime
    end: Optional[datetime]
    recurring: Optional[bool] = False
        
class event_response_schema(event_create_schema): #the server defines the response information, and responds with the matching id and user id
    id: str #using id instead of _id because mongo expects an objectId rather than a str, and fastapi can't expect objectIds, so we must convert _id to string in order for fastapi to be able to interpret the actual _id
    user_id: str
    created_at: datetime