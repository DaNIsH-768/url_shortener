from fastapi import HTTPException, APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
import jwt
import os
from ..database import get_session
from ..models import Urls, Clicks
from ..utils import to_base62, generate_unique_code
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

load_dotenv()

router = APIRouter()

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

'''async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])

        user_id = payload["user_id"]
        return user_id
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")
'''

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        user_id = payload["user_id"]
        return user_id
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")

class UrlParams(BaseModel):
    url:str = ""

@router.post("/urls", status_code=201)
def add_url(url_query: UrlParams, session: Session = Depends(get_session), user_id:int = Depends(get_current_user)):
    short_code = generate_unique_code(session)
    data = Urls(original_url=url_query.url, user_id=user_id, short_code=short_code)
    session.add(data)
    session.commit()

    return {
    "message": "URL shortened successfully",
    "short_code": short_code,
    "short_url": f"http://localhost:8000/{short_code}"
}

class RedirectParams(BaseModel):
    pass

@router.get("/{short_code}", status_code=301)
def redirect_user(short_code:str, request: Request, session: Session = Depends(get_session)):
    statment = select(Urls).where(Urls.short_code == short_code)
    results = session.exec(statment)
    res = results.first()

    if not res:
        raise HTTPException(status_code=404, detail="No such url exists")
    
    original_url = res.original_url

    click = Clicks(clicked_from=request.client.host, url_id=res.id)
    session.add(click)
    session.commit()
    return RedirectResponse(original_url)



