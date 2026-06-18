from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from ..main import app
from ..models import User
from ..database import get_session
from passlib.hash import bcrypt

TEST_DATABASE_URL = "sqlite:///test.db"
test_engine = create_engine(TEST_DATABASE_URL)

def override_get_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

def setup_module():
    SQLModel.metadata.create_all(test_engine)

def teardown_module():
    SQLModel.metadata.drop_all(test_engine)

client = TestClient(app)

def test_register_duplicate_email():
    with Session(test_engine) as s:
        user = User(email="mock@gmail.com", password="")
        s.add(user)
        s.commit()

    response = client.post('/auth/register',
    json= {
        "email": "mock@gmail.com",
        "password": "",
        "confirm_password": ""
    })

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}

def test_register_different_password():
    response = client.post('/auth/register',
    json= {
        "email": "test@gmail.com",
        "password": "a",
        "confirm_password": ""
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