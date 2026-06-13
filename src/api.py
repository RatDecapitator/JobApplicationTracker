from fastapi import FastAPI
from src.job_application_manager import JobApplicationManager
from src.job_application import JobApplication
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

manager = JobApplicationManager()


class JobApplicationCreate(BaseModel):
    company_name: str
    job_title: str
    location: str
    application_date: str
    cv_used: str


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
