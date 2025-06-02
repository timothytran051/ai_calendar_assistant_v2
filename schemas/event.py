from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class recurrence_pattern_schema(BaseModel):
    type: str #daily, weekly, absouteMonthly, relativeMonthly, absoluteYearly, etc.
    interval: int 
    days_of_week: Optional[List[str]] = None #only for weekly
    days_of_month: Optional[int] = None #only for monthly
    month: Optional[int] = None #yearly
    
class recurrence_range_schema(BaseModel):
    type: str #endDate, noEnd, numbered
    start_date: str #YYYY-MM-DD
    end_date: Optional[str] #YYYY-MM-DD
    occurences: Optional[int] = None #number of times event should repeat
    
class recurrence_schema(BaseModel):
    pattern: recurrence_pattern_schema
    range: recurrence_range_schema



class event_create_schema(BaseModel): #the client defines the information, containing data that is needed to create the event aka user input
    subject: str
    body: Optional[str]
    start: datetime
    end: Optional[datetime]
    recurring: Optional[recurrence_schema] = False
        
class event_response_schema(event_create_schema): #the server defines the response information, and responds with the matching id and user id
    id: str #using id instead of _id because mongo expects an objectId rather than a str, and fastapi can't expect objectIds, so we must convert _id to string in order for fastapi to be able to interpret the actual _id
    user_id: str
    created_at: datetime
    
    
