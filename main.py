from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from core.config import settings
from core.database import init_db
from routers import auth, chat, conversations, recipes


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

# CORS - pozwol frontendowi z innej domeny gadac z API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # w produkcji zawęź do swojej domeny
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routery API
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(conversations.router)
app.include_router(recipes.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


# Serwowanie frontendu
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")