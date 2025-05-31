import requests
from db.db import db
from datetime import datetime, timedelta

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