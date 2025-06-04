from fastapi import APIRouter, FastAPI
# from routes.auth import router as auth_router
from routes.events import router as events_router
from auth.oauth import router as oauth_router
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], #testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(events_router, prefix="/events", tags=["events"])
app.include_router(oauth_router, prefix="/oauth", tags=["oauth"])



handler = Mangum(app)