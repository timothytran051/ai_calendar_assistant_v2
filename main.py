from fastapi import APIRouter, FastAPI
from routes.auth import router as auth_router
from routes.events import router as events_router
from mangum import Mangum

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(events_router, prefix="/events", tags=["events"])

handler = Mangum(app)