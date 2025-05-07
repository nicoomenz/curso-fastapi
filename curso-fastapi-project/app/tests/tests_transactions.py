from fastapi.testclient import TestClient
from fastapi import status

def test_client(client):
    assert type(client) == TestClient

def test_transaction(client, customer):
    response = client.post(
        "/transactions/",
        json={
            "amount": 100.0,
            "description": "Test transaction",
            "customer_id": customer.id,
        },
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("amount") == 100.0
    assert response.json().get("description") == "Test transaction"

def test_get_transaction(client, customer):
    response = client.post(
        "/transactions/",
        json={
            "amount": 100.0,
            "description": "Test transaction",
            "customer_id": customer.id,
        },
    )
    response = client.get(
        "/transactions/",
    )

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == dict
    assert response.json().get("total") == 1