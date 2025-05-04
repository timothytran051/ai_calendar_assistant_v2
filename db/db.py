from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017") #currently local development need to switch later with azure based db
db = client["calendar_db"]