from flask import json


def _login(client):
    client.post(
        "/api/auth/register",
        json={"email": "user@example.com", "password": "password"},
    )
    return client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "password"},
    )


def test_create_category(client):
    login_response = _login(client)
    csrf_token = login_response.headers.get("Set-Cookie").split("csrf_token=")[1].split(";")[0]
    response = client.post(
        "/api/categories",
        json={"name": "Salary", "kind": "income"},
        headers={"X-CSRF-Token": csrf_token},
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["category"]["name"] == "Salary"
