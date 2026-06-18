import string
import random
from sqlmodel import Session, select
from .models import Urls

def to_base62(num: int):

    chars = string.digits + string.ascii_letters
    if num == 0:
        return chars[0]
    base62 = []
    while num > 0:
        num, rem = divmod(num, 62)
        base62.append(chars[rem])
    return "".join(reversed(base62))

def code_exists(short_code:str, session: Session):
    statement = select(Urls).where(Urls.short_code == short_code)
    result = session.exec(statement)
    res = result.first()

    if not res:
        return False
    
    return True


def get_random_str():
    chars = string.digits + string.ascii_letters

    char_list = random.choices(chars, k=7)
    return "".join(reversed(char_list))

def generate_unique_code(session: Session):

    while True:
        code = get_random_str()
        if not code_exists(code, session):
            return code
