from sqlmodel import Field, Session, SQLModel
from datetime import datetime

class user(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class urls(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    original_url: str 
    short_code: str = Field(unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user_id: int | None = Field(default=None, foreign_key="user.id")

class clicks(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    clicked_at: datetime = Field(default_factory=datetime.utcnow)
    clicked_from: str

    url_id: int | None = Field(default=None, foreign_key="urls.id")