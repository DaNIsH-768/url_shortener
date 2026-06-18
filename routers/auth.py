from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from passlib.hash import bcrypt
from database import engine
from models import User
import jwt
from datetime import datetime, timedelta
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class RegisterParams(BaseModel):
    email: str = ""
    password: str = ""
    confirm_password: str = ""

class LoginParams(BaseModel):
    email: str = ""
    password: str = ""

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

@router.post("/auth/register", status_code=201)
async def register(register_query: RegisterParams):

    if register_query.password != register_query.confirm_password:
        raise HTTPException(status_code=400, detail="Password do not match")

    if select_email(register_query.email):
        raise HTTPException(status_code=409, detail="Email already registered")

    h = bcrypt.hash(register_query.password)
    user = User(email = register_query.email, password = h)

    try:
        insert_user(user)
        return {"message": "User Registered Successfully"}
    except Exception as e:
        print(e)
        return {"message": "Error while registering"}


@router.post("/auth/login", status_code=200)
async def login(login_query: LoginParams):
    email, password = login_query.email, login_query.password

    user = select_email(email)

    if not user:
        raise HTTPException(status_code=400, detail="User not registered.")
    
    if not bcrypt.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Password incorrect.")

    exp = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))

    payload = {
        "user_id": user.id,
        "exp": exp
    }

    jwt_access = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

    return jwt_access



    

