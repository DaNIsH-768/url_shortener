import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from app.main import app
from app.database import get_session

TEST_DATABASE_URL = "sqlite:///test.db"
test_engine = create_engine(TEST_DATABASE_URL)

def override_get_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)

client = TestClient(app)