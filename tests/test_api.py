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


def test_update_application_status():
    response = client.patch(
        "/applications/2/status",
        json={"status": "Interview"},
    )

    assert response.status_code == 200

    application = client.get("/applications/2").json()

    assert application["status"] == "Interview"

    client.patch("/applications/2/status", json={"status": "Pending"})


def test_get_statistics():
    response = client.get("/statistics")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "pending" in data
    assert "accepted" in data
    assert "rejected" in data


def test_delete_application():
    create_response = client.post(
        "/applications",
        json={
            "company_name": "Delete Test Company",
            "job_title": "Test Role",
            "location": "Remote",
            "application_date": "2026-06-26",
            "cv_used": "CV_test",
        },
    )

    assert create_response.status_code == 200

    application = create_response.json()
    application_id = application["id"]

    delete_response = client.delete(f"/applications/{application_id}")

    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Application deleted"}

    get_response = client.get(f"/applications/{application_id}")

    assert get_response.status_code == 404


def test_add_company_response():
    create_response = client.post(
        "/applications",
        json={
            "company_name": "Response Test Company",
            "job_title": "Backend Developer",
            "location": "Remote",
            "application_date": "2026-06-26",
            "cv_used": "CV_test",
        },
    )

    assert create_response.status_code == 200

    application = create_response.json()
    application_id = application["id"]

    response = client.post(
        f"/applications/{application_id}/responses",
        json={
            "response_date": "2026-06-26",
            "content": "Recruiter replied by email.",
            "response_type": "Email",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Response added"}


def test_get_company_responses():
    create_response = client.post(
        "/applications",
        json={
            "company_name": "Responses Test",
            "job_title": "Python Developer",
            "location": "Remote",
            "application_date": "2026-06-26",
            "cv_used": "CV_test",
        },
    )

    application = create_response.json()
    application_id = application["id"]

    client.post(
        f"/applications/{application_id}/responses",
        json={
            "response_date": "2026-06-26",
            "content": "Invitation to interview.",
            "response_type": "Email",
        },
    )

    response = client.get(f"/applications/{application_id}/responses")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["content"] == "Invitation to interview."
    assert data[0]["response_type"] == "Email"
