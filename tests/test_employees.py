from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_employees():
    response = client.get("/employees/")

    assert response.status_code == 200


def test_create_employee(employee_data):
    response = client.post(
        "/employees/",
        json=employee_data
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "John"
    assert data["email"] == "john@test.com"
    assert data["department"] == "IT"
    assert data["salary"] == 50000
    assert data["age"] == 30
    assert "id" in data


def test_get_employee_not_found():
    response = client.get("/employees/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"

def test_create_employee_duplicate_email(employee_data):

    response1 = client.post("/employees/", json=employee_data)

    assert response1.status_code == 201

    response2 = client.post("/employees/", json=employee_data)

    assert response2.status_code == 409
    assert response2.json()["detail"] == "Employee already exists"

def test_create_employee_invalid_data():
    response = client.post(
        "/employees/",
        json={
            "name": "John",
            "email": "john@test.com",
            "department": "IT",
            "salary": "abc",
            "age": 30
        }
    )

    assert response.status_code == 422

def test_create_employee_missing_field():
    response = client.post(
        "/employees/",
        json={
            "name": "John",
            "department": "IT",
            "salary": 50000,
            "age": 30
        }
    )

    assert response.status_code == 422

#without create_employee_fixture
# def test_update_employee(employee_data):

#     create_response = client.post("/employees/", json=employee_data)

#     assert create_response.status_code == 201

#     employee_id = create_response.json()["id"]

#     update_response = client.put(
#         f"/employees/{employee_id}",
#         json={
#             "name": "John Updated",
#             "email": "john.updated@test.com",
#             "department": "Engineering",
#             "salary": 60000,
#             "age": 31
#         }
#     )

#     assert update_response.status_code == 200

#     data = update_response.json()

#     assert data["id"] == employee_id
#     assert data["name"] == "John Updated"
#     assert data["email"] == "john.updated@test.com"
#     assert data["department"] == "Engineering"
#     assert data["salary"] == 60000
#     assert data["age"] == 31

def test_update_employee(client, created_employee):
    employee_id = created_employee["id"]

    response = client.put(
        f"/employees/{employee_id}",
        json={
            "name": "John Updated",
            "email": "john.updated@test.com",
            "department": "Engineering",
            "salary": 60000,
            "age": 31
        }
    )

    assert response.status_code == 200

#without create_employee_fixture
# def test_delete_employee(employee_data):
 
#     create_response = client.post("/employees/", json=employee_data)

#     assert create_response.status_code == 201

#     employee_id = create_response.json()["id"]

#     delete_response = client.delete(
#         f"/employees/{employee_id}"
#     )

#     assert delete_response.status_code == 200

#     # Verify employee no longer exists
#     get_response = client.get(
#         f"/employees/{employee_id}"
#     )

#     assert get_response.status_code == 404

def test_delete_employee(client, created_employee):
    employee_id = created_employee["id"]

    response = client.delete(
        f"/employees/{employee_id}"
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/employees/{employee_id}"
    )

    assert get_response.status_code == 404