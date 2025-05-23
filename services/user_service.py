import requests
from db.db import db

def get_user_info(access_token):    
    graph_url = "https://graph.microsoft.com/v1.0/me"
    data = requests.get(graph_url, headers={"Authorization": f"Bearer {access_token}"}) #uses access token to retrieve data from microsoft graph /me
    response_data = data.json() #includes user table data
    user_data = {
        "_id": response_data["id"], #retrieves id
        "displayName": response_data.get("displayName"), #get makes parameter optional
        "email": response_data.get("mail"),
        "username": response_data.get("userPrincipalName")
    }
    return user_data
    
    
async def upsert_user(user_data): #upsert function (insert or update)
    users_collection = db["users"]
    await users_collection.update_one(
        {"_id": user_data["_id"]},
        {"$set": user_data},
        upsert=True
    )