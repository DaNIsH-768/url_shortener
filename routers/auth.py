from fastapi import APIRouter
from sqlmodel import Session, select
from passlib.hash import bcrypt
from database import engine
from models import User
from pydantic import BaseModel

router = APIRouter()

class RegisterParams(BaseModel):
    email: str = ""
    password: str = ""
    confirm_password: str = ""

def select_email(email:str):
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        result = session.exec(statement)
        res = result.first()

        return res

def insert_user(user:User):
    with Session(engine) as session:

        session.add(user)
        session.commit()

@router.post("/auth/register")
async def register(register_query: RegisterParams):

    if register_query.password != register_query.confirm_password:
        return {"message": "Passwords do not match."}

    if select_email(register_query.email):
        return {"message": "Email already registered."}

    h = bcrypt.hash(register_query.password)
    user = User(email = register_query.email, password = h)

    try:
        insert_user(user)
        return {"message": "User Registered Successfully"}
    except Exception as e:
        print(e)
        return {"message": "Error while registering"}

    

