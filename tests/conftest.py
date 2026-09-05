import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app


TEST_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/fastapi_employee_test"

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def employee_data():
    return {
        "name": "John",
        "email": "john@test.com",
        "department": "IT",
        "salary": 50000,
        "age": 30
    }


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def created_employee(client, employee_data):
    response = client.post(
        "/employees/",
        json=employee_data
    )

    assert response.status_code == 201

    return response.json()