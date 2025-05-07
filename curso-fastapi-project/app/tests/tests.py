from fastapi.testclient import TestClient
from models import Customer

def test_client(client):
    assert type(client) == TestClient