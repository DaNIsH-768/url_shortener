from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_register_invalid_email():
    response = client.post('/auth/register',
    json= {
        "email": "test@gmail.com",
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
