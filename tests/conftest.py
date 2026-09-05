import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth.auth import hash_password
from database import Base, get_db
from main import app
from models import User


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
def client():
    return TestClient(app)


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
def admin_user():
    db = TestingSessionLocal()

    user = User(
        email="admin@test.com",
        password_hash=hash_password("admin123"),
        role="admin",
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    db.close()

    return user


@pytest.fixture
def admin_token(client, admin_user):
    response = client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "admin123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def auth_headers(admin_token):
    return {
        "Authorization": f"Bearer {admin_token}"
    }


@pytest.fixture
def created_employee(client, employee_data, auth_headers):
    response = client.post(
        "/employees/",
        json=employee_data,
        headers=auth_headers
    )

    assert response.status_code == 201

    return response.json()