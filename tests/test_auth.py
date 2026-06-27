from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from app.main import app
from app.models import User
from app.database import get_session
from .conftest import client, test_engine
from passlib.hash import bcrypt

def test_register_duplicate_email():
    with Session(test_engine) as s:
        user = User(email="mock@gmail.com", password="password")
        s.add(user)
        s.commit()

    print(client.get("/health").status_code)

    response = client.post('/auth/register',
    json= {
        "email": "mock@gmail.com",
        "password": "password",
        "confirm_password": "password"
    })

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}

def test_register_different_password():
    response = client.post('/auth/register',
    json= {
        "email": "test@gmail.com",
        "password": "password",
        "confirm_password": "password1"
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "Password do not match"}

def test_register_success():
    response = client.post('/auth/register',
    json= {
        "email": "test@gmail.com",
        "password": "password",
        "confirm_password": "password"
    })

    assert response.status_code == 201
    assert response.json() == {"message": "User Registered Successfully"}

def test_login_user_not_registered():
    h = bcrypt.hash("password")
    response = client.post('/auth/login', 
    json = {
        "email": "mocked@gmail.com",
        "password": h
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "User not registered."}

def test_login_invalid_password():
    h = bcrypt.hash("password")
    with Session(test_engine) as s:
        user = User(email="mocked@gmail.com", password=h)
        s.add(user)
        s.commit()

    response = client.post('/auth/login', 
    json = {
        "email": "mocked@gmail.com",
        "password": "incorrect"
    })

    assert response.status_code == 401
    assert response.json() == {"detail": "Password incorrect."}

def test_login_success():
    response = client.post('/auth/login', 
    json = {
        "email": "mocked@gmail.com",
        "password": "password"
    })

    assert response.status_code == 200