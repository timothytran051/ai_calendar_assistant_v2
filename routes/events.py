# from main import events_router as router
from fastapi import APIRouter, Request
from schemas.event import event_create_schema, event_response_schema, event_update_schema
from db.db import db
from services.user_service import token_validation
from datetime import datetime
import requests
import uuid

router = APIRouter()

@router.get("")
async def get_events(user_id: str):
    event_collection = db["events"]
    user_collection = db["users"]
    # user_id = user_collection["_id"]
    token_validation(user_id)
    
    cursor = event_collection.find({"user_id": user_id}) #creates a cursor to find matching user_id in events table
    events = await cursor.to_list(length=None) #converts the cursor to a list
    return events
    
    
@router.post("", response_model=event_response_schema)
async def create_event(event: event_create_schema, user_id: str):
    event_data = event.dict() #turns event response into python dict
    event_collection = db["events"] #establish connection with db and events table
    user_collection = db["users"]
    # user_id = user_collection["_id"] #use only for now, later on will change to localstorage on browser
    token_validation(user_id) #validates token and refreshes if needed
    
    # event_data = {
    #     "user_id": "",  # hardcoded for now
    #     "created_at": datetime.utcnow(),
    #     "subject": "Example Event",
    #     "body": "Description of the event",
    #     "start": datetime.utcnow(),
    #     "end": datetime.utcnow(),
    #     "recurring": None
    # }
    event_data["event_id"] = str(uuid.uuid4())
    await event_collection.insert_one(event_data)
    
    # headers = {
    #     "Authorization": access_token,
    #     "Content-Type": "application/json"
    # }
    # graph_url = "https://graph.microsoft.com/v1.0/me"
    # response = requests.get(graph_url, headers=headers)
    # print(response.status_code, response.json())
    
    # await event_collection.insert_one(event_data)
    
    return event_data
    
    
@router.patch("/{event_id}")
async def update_event(event_id, update: event_update_schema, user_id: str):
    new_event = update.dict()
    update_fields = {}
    for key, value in new_event.items(): #for loop goes through data from requests and removes all instances of None
        if value is not None:
            update_fields[key] = value
            
    event_collection = db["events"]
    user_collection = db["users"]
    token_validation(user_id)
    await event_collection.update_one({"event_id": event_id, "user_id": user_id}, {"$set": update_fields})
    
@router.delete("/{event_id}")
async def delete_event(event_id, user_id: str):
    event_collection = db["events"]
    user_collection = db["users"]
    token_validation(user_id)
    await event_collection.find_one_and_delete({"event_id": event_id, "user_id": user_id})
    
    
#1) user logs in and enters /events page
#2) frontend stores token
#3) using stored token, sends request
#4) backend decodes token and extracts graph /me data (specifically user_id)
#5) finds corresponding user in user table 
#6) performs requests using user_id