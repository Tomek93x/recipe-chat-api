from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.config import settings
from core.database import init_db
from routers import chat, conversations


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(chat.router)
app.include_router(conversations.router)


@app.get("/")
async def root():
    return {"message": "Recipe Chat API is running"}