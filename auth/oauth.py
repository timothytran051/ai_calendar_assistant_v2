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
from services.user_service import get_user_info
import requests

router = APIRouter()

load_dotenv()
client_id = os.getenv("APP_ID")
redirect_uri = os.getenv("REDIRECT_URI")
secret = os.getenv("CLIENT_SECRET")

@router.get("/login") #get request, /auth/login
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
def decode(request: Request): #receives query parameter [ex) ?code=0.AAAA1XyZ...abc123]
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
    print("Access Token:", access_token)
    print("data:", response_data)
    get_user_info(access_token)
    
    
    
    
#NEXT STEPS
#learn mongodb and connections
#create user table in mongo
#update user table with /me payload
