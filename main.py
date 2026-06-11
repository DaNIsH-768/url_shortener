from fastapi import FastAPI
from database import initialise_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialise_db()
    yield


app = FastAPI(
    title="URL Shortener API",
    description="A URL shortening service with analytics",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/health")
def health():
    return {"status": "ok"}
