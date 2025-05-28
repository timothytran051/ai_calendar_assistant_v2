# from main import events_router as router
from fastapi import APIRouter
from schemas.event import event_create_schema, event_response_schema
from db.db import db

router = APIRouter()

# @router.get("")
# async def events():
    
    
    
@router.post("", response_model=event_response_schema)
async def create_event(event: event_create_schema):
    event_data = event.dict() #turns event response into python dict
    event_collection = db["events"] #establish connection with db and events table
    # user_collection = db["users"]
    await event_collection.insert_one(event_data)
    
# 1) it needs to make sure that the user is logged in and the token is still valid from microsoft
# 2) it needs to receive the data from the frontend as json data i believe and it should look like the response_model=event_create_schema **not create, response schema
# 3) i dont think it needs to make sure that a event already exists, since i could have multiple of the same event on different days
# 4) it needs to know whether its a recurring event or just a one time event
# 5) it needs to actually create the event and update the db
# 6) it needs to display the new data, maybe using commit and refresh