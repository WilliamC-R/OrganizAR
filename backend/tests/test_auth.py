from flask import json


def test_register_and_login(client):
    response = client.post(
        "/api/auth/register",
        json={"email": "user@example.com", "password": "password"},
    )
    assert response.status_code == 201

    response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "password"},
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["user"]["email"] == "user@example.com"
