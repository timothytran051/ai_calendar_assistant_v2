# from main import oauth_router as router
from fastapi import APIRouter, Depends, HTTPException, Request
# from models.user import MicrosoftUser
# from sqlalchemy.ext.asyncio import AsyncSession
# from db.base import get_db
from dotenv import load_dotenv
import os
from urllib.parse import urlencode
from fastapi.responses import RedirectResponse
import json
from motor.motor_asyncio import AsyncIOMotorClient
from db.db import db
from services.user_service import get_user_info, upsert_user
import requests

router = APIRouter()

load_dotenv()
client_id = os.getenv("APP_ID")
redirect_uri = os.getenv("REDIRECT_URI")
secret = os.getenv("CLIENT_SECRET")

@router.get("/login") #get request, /oauth/login
def microsoft_login(): #login function
    auth_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize" #starting point for microsoft oauth login
    params = { #parameters used in url
        "client_id": client_id, #app identity
        "response_type": "code", #requests authorization code, NOT token
        "redirect_uri": redirect_uri, #redirects user to uri (currently http://localhost:8000/oauth/microsoft/callback)
        "scope": "User.Read offline_access Calendars.ReadWrite", #user grants access for app
        "response_mode": "query" #microsoft returns code in URL query string
    }
    url = f"{auth_url}?{urlencode(params)}" #combines auth_url with parameters
    return RedirectResponse(url) #fastapi redirects user to microsoft login screen

@router.get("/microsoft/callback") #token exchange function, makes request/handles callback
async def decode(request: Request): #receives query parameter [ex) ?code=0.AAAA1XyZ...abc123]
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token" #microsoft token endpoint, function will send POST request to this URL to exchange the code for an access token
    params = { 
        "client_id": client_id, #app identity
        "client_secret": secret, #client secret from azure
        "grant_type": "authorization_code", #defines what function gives to microsoft, in this case the "authorization_code" is obtained from user login, then is "exchanged" for an access token from microsoft
        "code": request.query_params.get("code"), #extracts code microsoft sent via query param
        "redirect_uri": redirect_uri, #redirects user to uri
        "scope": "User.Read offline_access Calendars.ReadWrite" #same as login route
    }
    body = urlencode(params)
    
    data = requests.post(token_url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"}) #sends post request
    response_data = data.json() #translates request to python dictionary
    access_token = response_data["access_token"] #extracts access token from response
    refresh_token = response_data["refresh_token"]
    expires_in = response_data["expires_in"]
    token_data = { #combines token data into a python dict
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": expires_in
    }
    info = get_user_info(token_data)
    redirect = f"http://localhost:8080/?access_token={access_token}&user_id={info['_id']}"
    await upsert_user(info)
    return RedirectResponse(redirect)

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
        
    if response.status_code not in [200,401]:
        raise HTTPException(status_code=500, detail="Microsoft Graph error during token validation.")
    
    return access_token #sends new access token back to where function is called