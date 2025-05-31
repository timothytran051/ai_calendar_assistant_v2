# from main import events_router as router
from fastapi import APIRouter, HTTPException
from schemas.event import event_create_schema, event_response_schema
from db.db import db
import requests
from urllib.parse import urlencode

router = APIRouter()

# @router.get("")
# async def events():
    
    
    
@router.post("", response_model=event_response_schema)
async def create_event(event: event_create_schema):
    event_data = event.dict() #turns event response into python dict
    event_collection = db["events"] #establish connection with db and events table
    user_collection = db["users"]
    
    await event_collection.insert_one(event_data)
    
    
async def token_validation(user_id: str) -> str:
    graph_url = "https://graph.microsoft.com/v1.0/me"
    user_collection = db["users"]
    access_token = user_collection["access_token"]
    user_id = user_collection["_id"]
    refresh_token = user_collection["refresh_token"]
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    try:
        data = requests.get(graph_url, headers={"Authorization": f"Bearer {access_token}"})
    except HTTPException as e:
        if e.status_code == 401:
            params = {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "scope": "User.Read offline_access Calendars.ReadWrite"
            }
            body = urlencode(params)
            data = requests.post(token_url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    
# 1) it needs to make sure that the user is logged in and the token is still valid from microsoft
# 2) it needs to receive the data from the frontend as json data i believe and it should look like the response_model=event_create_schema **not create, response schema
# 3) i dont think it needs to make sure that a event already exists, since i could have multiple of the same event on different days
# 4) it needs to know whether its a recurring event or just a one time event
# 5) it needs to actually create the event and update the db
# 6) it needs to display the new data, maybe using commit and refresh