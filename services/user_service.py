import requests
from db.db import db
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import requests
from fastapi import HTTPException
from urllib.parse import urlencode

load_dotenv()
client_id = os.getenv("APP_ID")
redirect_uri = os.getenv("REDIRECT_URI")
secret = os.getenv("CLIENT_SECRET")

def get_user_info(token_data):    
    graph_url = "https://graph.microsoft.com/v1.0/me"
    access_token = token_data["access_token"]
    data = requests.get(graph_url, headers={"Authorization": f"Bearer {access_token}"}) #uses access token to retrieve data from microsoft graph /me
    response_data = data.json() #includes user table data
    user_data = {
        "_id": response_data["id"], #retrieves id
        "displayName": response_data.get("displayName"), #get makes parameter optional
        "email": response_data.get("mail"),
        "username": response_data.get("userPrincipalName"),
        "access_token": token_data.get("access_token"),
        "refresh_token": token_data.get("refresh_token"),
        "expires_in": token_data.get("expires_in")
    }
    return user_data
    
    
async def upsert_user(user_data): #upsert function (insert or update)
    users_collection = db["users"] #creates or "opens" users table in db
    await users_collection.update_one( 
        {"_id": user_data["_id"]}, #grabs user id from table, if found then mongo will go to next step, if not then it will create an _id
        {"$set": user_data}, #updates or inserts user data
        # {"refresh_token": refresh}, #refresh token for when the users access token expires. 
        #                             #this token will be used instead to keep the user from having to log in again
        # {"token_expiry": datetime.utcnow() + timedelta(seconds = expire)}, #token expiration translated to a 
        upsert=True #update or insert
    )
    
async def token_validation(user_id: str) -> str:
    graph_url = "https://graph.microsoft.com/v1.0/me"
    user_collection = db["users"] #opens user table
    user_info = await user_collection.find_one({"_id": user_id}) #looks through table to match existing _id from inside table to current user's user_id
    access_token = user_info.get("access_token") #retrieves access token
    refresh_token = user_info.get("refresh_token") #retrieves refresh token
    # access_token = user_collection["access_token"]
    # user_id = user_collection["_id"]
    # refresh_token = user_collection["refresh_token"]
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    # try:
    response = requests.get(graph_url, headers={"Authorization": f"Bearer {access_token}"}) #makes get request to /me
    # except HTTPException as e:
    if response.status_code == 401: #if /me responds with error 401 (unauthorized token), then use refresh token to generate new access token
        params = {
            "client_id": client_id,
            "client_secret": secret,
            "grant_type": "refresh_token", #token exchange, in this case refresh token for access token exchange
            "refresh_token": refresh_token, #takes refresh token from above exchange and inputs into refresh_token variable
            "scope": "User.Read offline_access Calendars.ReadWrite"
        }
        body = urlencode(params)
        data = requests.post(token_url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"}) #sends refresh token request
        refresh_data = data.json()
        new_token = get_user_info(refresh_data) #retrieves user data
        await upsert_user(new_token) #updates user data with new access token
        access_token = refresh_data["access_token"]
    return access_token #sends new access token back to where function is called