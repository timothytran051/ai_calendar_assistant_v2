from fastapi import requests
from db.db import db

def get_user_info(access_token):    
    graph_url = "https://graph.microsoft.com/v1.0/me"
    data = requests.get(graph_url, headers={f"Authorization: Bearer {access_token}"}) #uses access token to retrieve data from microsoft graph /me
    response_data = data.json() #includes user table data
    user_data = {
        "_id": response_data["id"],
        "displayName": response_data.get("displayName"),
        "email": response_data.get("mail"),
        "username": response_data.get("userPrincipalName")
    }
    
    await db["users"].update_one(
        
    )