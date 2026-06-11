# used for testing

from src.job_application import JobApplication
from src.job_application_manager import JobApplicationManager
from src.application_status import ApplicationStatus

application = JobApplication(
    "Google",
    "Backend Developer",
    "Warsaw",
    "2026-06-11",
    "CV_v1",
)

manager = JobApplicationManager()
manager.add_application(application)

print(manager.applications)
print(manager.applications[0].company_name)
print(manager.applications[0].status.value)
