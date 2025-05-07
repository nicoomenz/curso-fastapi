from fastapi.testclient import TestClient
from fastapi import status

def test_client(client):
    assert type(client) == TestClient

def test_customer(client):
    response = client.post(
        "/customers/",
        json={
            "name": "John Doe",
            "description": "Test customer",
            "email": "nicoomenz@gmail.com",
            "age": 30,
        },
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("name") == "John Doe"

def test_read_customer(client):
    response = client.post(
        "/customers/",
        json={
            "name": "John Doe",
            "description": "Test customer",
            "email": "nicoomenz@gmail.com",
            "age": 30,
        },
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    response = client.get(
        f"/customers/{response.json().get('id')}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("name") == "John Doe"