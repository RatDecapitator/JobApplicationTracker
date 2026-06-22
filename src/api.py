from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.application_status import ApplicationStatus
from src.job_application_manager import JobApplicationManager
from src.job_application import JobApplication
from src.company_response import CompanyResponse
from src.response_type import ResponseType

app = FastAPI()

manager = JobApplicationManager()


class JobApplicationCreate(BaseModel):
    company_name: str
    job_title: str
    location: str
    application_date: str
    cv_used: str


class JobApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus


class CompanyResponseCreate(BaseModel):
    response_date: str
    content: str
    response_type: ResponseType


manager.add_application(
    JobApplication(
        "Google",
        "Backend Developer",
        "Warsaw",
        "2026-06-13",
        "CV_v1",
    )
)


@app.get("/")
def root():
    return {"message": "Job Application Tracker API"}


@app.get("/applications")
def get_applications():
    return manager.get_all_applications()


@app.get("/applications/{application_id}")
def get_application(application_id: int):
    application = manager.find_application(application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application


@app.post("/applications")
def create_application(application_data: JobApplicationCreate):
    application = JobApplication(
        application_data.company_name,
        application_data.job_title,
        application_data.location,
        application_data.application_date,
        application_data.cv_used,
    )

    manager.add_application(application)

    return application


@app.delete("/applications/{application_id}")
def delete_application(application_id: int):
    application = manager.find_application(application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    manager.remove_application(application_id)

    return {"message": "Application deleted"}


@app.patch("/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    status_update: JobApplicationStatusUpdate,
):
    application = manager.find_application(application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    application.change_status(status_update.status)

    return application


@app.post("/applications/{application_id}/responses")
def add_company_response(
    application_id: int,
    response_data: CompanyResponseCreate,
):
    application = manager.find_application(application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    response = CompanyResponse(
        response_data.response_date, response_data.content, response_data.response_type
    )

    application.add_response(response)

    return application

@app.get("/applications/{application_id}/responses")
def get_company_responses(application_id: int):
    application = manager.find_application(application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return application.responses