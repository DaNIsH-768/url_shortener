from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from passlib.hash import bcrypt
from ..database import engine, get_session
from ..models import User
import jwt
from datetime import datetime, timedelta
import os
from pydantic import BaseModel, EmailStr, Field
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class RegisterParams(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str = ""

class LoginParams(BaseModel):
    email: str = ""
    password: str = ""

def select_email(email:str, session: Session):
    statement = select(User).where(User.email == email)
    result = session.exec(statement)
    res = result.first()

    return res

def insert_user(user:User, session: Session):
    session.add(user)

@router.post("/auth/register", status_code=201)
async def register(register_query: RegisterParams, session: Session = Depends(get_session)):

    if register_query.password != register_query.confirm_password:
        raise HTTPException(status_code=400, detail="Password do not match")

    if select_email(register_query.email, session):
        raise HTTPException(status_code=409, detail="Email already registered")

    h = bcrypt.hash(register_query.password)
    user = User(email = register_query.email, password = h)

    try:
        insert_user(user, session)
        session.commit()
        return {"message": "User Registered Successfully"}
    except Exception as e:
        print(e)
        return {"message": "Error while registering"}


@router.post("/auth/login", status_code=200)
async def login(login_query: LoginParams, session: Session = Depends(get_session)):
    email, password = login_query.email, login_query.password

    user = select_email(email, session)

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



    

