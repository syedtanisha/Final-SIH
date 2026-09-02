import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "MoSPI" in data["ecosystem"]
    assert data["status"] == "Online"

def test_user_registration_and_login():
    email = "test_iss_officer@gov.in"
    reg_payload = {
        "email": email,
        "password": "SecurePassword123!",
        "full_name": "Dr. Rajesh Kumar",
        "designation": "Deputy Director",
        "department": "National Accounts Division",
        "organization": "MoSPI"
    }
    # Register
    res = client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code in [201, 400] # 201 if first time, 400 if duplicate

    # Login
    login_res = client.post("/api/v1/auth/login/json", json={
        "username": email,
        "password": "SecurePassword123!"
    })
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "Bearer"

    # Profile Me
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == email
