from .conftest import client, test_engine
from sqlmodel import Session, select
from app.models import User, Urls


def get_token(email: str, password: str):
    client.post('/auth/register', json={
        "email": email,
        "password": password,
        "confirm_password": password
    })
    
    response = client.post('/auth/login', json={
        "email": email,
        "password": password
    })
    
    return response.json()

def get_short_code(url: str):
    token = get_token("urltest@gmail.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post('/urls', 
    json = {
        'url': 'https://www.google.com'
    }, headers=headers)

    res = response.json()
    return res['short_code']

def test_create_url_success():
    token = get_token("urltest@gmail.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post('/urls', 
    json = {
        'url' : 'https://www.google.com'
    }, headers = headers)

    assert response.status_code == 201
    assert "short_code" in response.json()
    assert "short_url" in response.json()


def test_create_url_unauthenticated():
    token = get_token("urltest@gmail.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post('/urls', 
    json = {
        'url' : 'https://www.google.com'
    })

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

def test_redirect_success():
    token = get_token("redirect@gmail.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}
    
    create_response = client.post("/urls", 
        json={"url": "https://www.google.com"},
        headers=headers
    )

    short_code = create_response.json()["short_code"]
    
    response = client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code == 301
    assert "google.com" in response.headers["location"]


def test_url_invalid_code():
    code = 'abcd'

    res = client.get('/{code}')

    assert res.status_code == 404
    assert res.json() == {'detail': 'No such url exists'}


def test_get_urls_success():
    token = get_token("redirect@gmail.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get('/urls', headers = headers)

    assert res.status_code == 200
    assert len(res.json()) > 0


def test_get_urls_unauthenticated():
    res = client.get('/urls')

    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}


def test_analytics_success():
    token = get_token("analytics@gmail.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post("/urls", 
        json={"url": "https://www.google.com"},
        headers=headers
    )

    short_code = create_response.json()["short_code"]
    res = client.get(f'/analytics/{short_code}', headers=headers)

    assert res.status_code == 200
    assert "total_clicks" in res.json()
    assert "unique_sources" in res.json()


def test_analytics_forbidden():
    user_a = get_token("analytics1@gmail.com", "password123")
    user_a_headers = {"Authorization": f"Bearer {user_a}"}

    user_b = get_token("analytics2@gmail.com", "password123")
    user_b_headers = {"Authorization": f"Bearer {user_b}"}

    create_response = client.post("/urls", 
        json={"url": "https://www.google.com"},
        headers=user_a_headers
    )

    short_code = create_response.json()["short_code"]
    res = client.get(f'/analytics/{short_code}', headers=user_b_headers)

    assert res.status_code == 403
    assert res.json() == {'detail': 'Forbidden'}

