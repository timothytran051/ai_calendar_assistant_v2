from main import oauth_router as router
from fastapi import APIRouter, Depends, HTTPException, Request
from models.user import MicrosoftUser
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import get_db
from dotenv import load_dotenv
import os
from urllib.parse import urlencode
from fastapi.responses import RedirectResponse

router = APIRouter()

load_dotenv()
client_id = os.getenv("APP_ID")
redirect_uri = os.getenv("REDIRECT_URI")
secret = os.getenv("CLIENT_SECRET")

@router.get("/login") #login function, 
def microsoft_login():
    auth_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "User.Read offline_access Calendars.ReadWrite",
        "response_mode": "query"
    }
    url = f"{auth_url}?{urlencode(params)}"
    return RedirectResponse(url)

@router.get("/microsoft/callback") #token exchange function, makes request 
def decode(request: Request):
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    params = {
        "client_id": client_id,
        "client_secret": secret,
        "grant_type": "authorization_code",
        "code": request.query_params.get("code"),
        "redirect_uri": redirect_uri,
        "scope": "User.Read offline_access Calendars.ReadWrite"
    }
    url = f"{token_url}?{urlencode(params)}"
    