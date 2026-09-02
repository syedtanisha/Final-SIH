import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.models.models import User
from app.core.security import create_access_token

client = TestClient(app)

def test_unauthenticated_admin_stats_access():
    res = client.get("/api/v1/admin/stats")
    assert res.status_code == 401

def test_regular_user_forbidden_from_admin_stats():
    db = SessionLocal()
    try:
        regular_user = db.query(User).filter(User.email == "regular_user_test@mospi.gov.in").first()
        if not regular_user:
            regular_user = User(
                email="regular_user_test@mospi.gov.in",
                hashed_password="fakehashpassword",
                full_name="Regular Field Officer",
                designation="Junior Statistical Officer",
                department="FOD",
                role="user"
            )
            db.add(regular_user)
            db.commit()
            db.refresh(regular_user)
        else:
            regular_user.role = "user"
            db.commit()

        token = create_access_token({"sub": str(regular_user.id)})
        headers = {"Authorization": f"Bearer {token}"}
        
        res = client.get("/api/v1/admin/stats", headers=headers)
        assert res.status_code == 403
        assert "Admin privileges required" in res.json()["detail"]
    finally:
        db.close()

def test_admin_user_authorized_for_admin_stats():
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.email == "system_admin_test@mospi.gov.in").first()
        if not admin_user:
            admin_user = User(
                email="system_admin_test@mospi.gov.in",
                hashed_password="fakehashpassword",
                full_name="Chief System Administrator",
                designation="Director General",
                department="MoSPI Headquarters",
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
        else:
            admin_user.role = "admin"
            db.commit()

        token = create_access_token({"sub": str(admin_user.id)})
        headers = {"Authorization": f"Bearer {token}"}
        
        res = client.get("/api/v1/admin/stats", headers=headers)
        assert res.status_code == 200
        data = res.json()
        assert "total_officers_registered" in data
        assert "total_statistical_competencies" in data
        assert data["status"] == "Operational"
    finally:
        db.close()
