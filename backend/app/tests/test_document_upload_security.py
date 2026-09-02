import io
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_token():
    email = "upload_tester@mospi.gov.in"
    reg_payload = {
        "email": email,
        "password": "SecurePassword123!",
        "full_name": "Upload Tester",
        "designation": "Statistical Officer",
        "department": "FOD",
        "organization": "MoSPI"
    }
    client.post("/api/v1/auth/register", json=reg_payload)
    login_res = client.post("/api/v1/auth/login/json", json={
        "username": email,
        "password": "SecurePassword123!"
    })
    return login_res.json()["access_token"]

def test_upload_disallowed_file_extensions():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    disallowed = [
        ("malicious_script.exe", b"MZ\x90\x00BinaryExeContent"),
        ("archive.zip", b"PK\x03\x04ZipContent"),
        ("script.bat", b"@echo off\necho hello"),
        ("deploy.sh", b"#!/bin/bash\necho hello"),
        ("script.py", b"print('hello')"),
    ]
    for filename, content in disallowed:
        files = {"file": (filename, io.BytesIO(content), "application/octet-stream")}
        res = client.post("/api/v1/documents/upload", files=files, headers=headers)
        assert res.status_code == 400
        assert "Unsupported file format" in res.json()["detail"]

def test_upload_file_without_extension():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    files = {"file": ("unnamed_file", io.BytesIO(b"Some plain text content"), "text/plain")}
    res = client.post("/api/v1/documents/upload", files=files, headers=headers)
    assert res.status_code == 400
    assert "File has no extension" in res.json()["detail"]

def test_upload_empty_file():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    files = {"file": ("empty_notes.txt", io.BytesIO(b""), "text/plain")}
    res = client.post("/api/v1/documents/upload", files=files, headers=headers)
    assert res.status_code == 400
    assert "empty" in res.json()["detail"].lower()

def test_upload_oversized_file():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # 26 MB (exceeds 25 MB limit)
    oversized_content = b"0" * (26 * 1024 * 1024)
    files = {"file": ("oversized_notes.txt", io.BytesIO(oversized_content), "text/plain")}
    res = client.post("/api/v1/documents/upload", files=files, headers=headers)
    assert res.status_code == 400
    assert "25MB" in res.json()["detail"]

def test_upload_valid_text_document():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    valid_content = (
        "Ministry of Statistics and Programme Implementation (MoSPI) technical note on National Quality Assurance Framework. "
        "Standardized validation rules are enforced across all regional data collection centers to ensure high integrity statistics."
    ).encode("utf-8")
    
    files = {"file": ("mospi_nqaf_notes.txt", io.BytesIO(valid_content), "text/plain")}
    res = client.post("/api/v1/documents/upload", files=files, headers=headers)
    assert res.status_code == 201
    data = res.json()
    assert data["filename"] == "mospi_nqaf_notes.txt"
    assert data["file_type"] == "txt"
    assert data["character_count"] > 50
    assert "preview_text" in data
