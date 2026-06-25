from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.application_status import ApplicationStatus
from src.job_application import JobApplication
from src.company_response import CompanyResponse
from src.response_type import ResponseType
from src.database import (
    create_tables,
    save_application,
    get_all_applications_from_db,
    get_application_by_id,
    delete_application_by_id,
    update_application_status as update_application_status_in_db,
    save_company_response,
    get_responses_for_application,
    get_application_statistics,
)

app = FastAPI()
create_tables()


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


class JobApplicationResponse(BaseModel):
    id: int
    company_name: str
    job_title: str
    location: str
    application_date: str
    cv_used: str
    status: str


class CompanyResponseResponse(BaseModel):
    id: int
    application_id: int
    response_date: str
    content: str
    response_type: str


class StatisticsResponse(BaseModel):
    total: int
    pending: int
    accepted: int
    rejected: int


@app.get("/")
def root():
    return {"message": "Job Application Tracker API"}


@app.get("/applications", response_model=list[JobApplicationResponse])
def get_applications():
    return get_all_applications_from_db()


@app.get("/applications/{application_id}", response_model=JobApplicationResponse)
def get_application(application_id: int):
    application = get_application_by_id(application_id)

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

    application_id = save_application(application)

    return get_application_by_id(application_id)


@app.delete("/applications/{application_id}")
def delete_application(application_id: int):
    application = get_application_by_id(application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    delete_application_by_id(application_id)

    return {"message": "Application deleted"}


@app.patch("/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    status_update: JobApplicationStatusUpdate,
):
    application = get_application_by_id(application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    update_application_status_in_db(
        application_id,
        status_update.status.value,
    )

    return {"message": "Status updated"}


@app.post("/applications/{application_id}/responses")
def add_company_response(
    application_id: int,
    response_data: CompanyResponseCreate,
):
    application = get_application_by_id(application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    response = CompanyResponse(
        response_data.response_date,
        response_data.content,
        response_data.response_type,
    )

    save_company_response(application_id, response)

    return {"message": "Response added"}


@app.get(
    "/applications/{application_id}/responses",
    response_model=list[CompanyResponseResponse],
)
def get_company_responses(application_id: int):
    application = get_application_by_id(application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return get_responses_for_application(application_id)


@app.get("/statistics", response_model=StatisticsResponse)
def get_statistics():
    return get_application_statistics()
