from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Job Application Tracker API"}


def test_get_applications():
    response = client.get("/applications")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_application_by_id():
    response = client.get("/applications/2")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 2
    assert data["company_name"] == "Gwiezdna Flota"
    assert data["status"] == "Pending"


def test_get_application_not_found():
    response = client.get("/applications/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}


def test_create_application():
    response = client.post(
        "/applications",
        json={
            "company_name": "OpenAI",
            "job_title": "Python Developer",
            "location": "Remote",
            "application_date": "2026-06-25",
            "cv_used": "CV_v3",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company_name"] == "OpenAI"
    assert data["job_title"] == "Python Developer"
    assert data["status"] == "Pending"
