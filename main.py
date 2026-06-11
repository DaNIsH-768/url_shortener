from fastapi import FastAPI
from sqlmodel import create_engine
import os
from dotenv import load_dotenv

app = FastAPI(
    title="URL Shortener API",
    description="A URL shortening service with analytics",
    version="0.1.0"
)

load_dotenv()

connect_args = {"check_same_thread": False}
engine = create_engine(os.environ["DATABASE_URL"], connect_args=connect_args)

@app.get("/health")
def health():
    return {"status": "ok"}