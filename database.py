from sqlmodel import Field, SQLModel, create_engine, Session
import os
from dotenv import load_dotenv
from .models import User, Urls, Clicks

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment or .env")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def initialise_db():
    SQLModel.metadata.create_all(engine)