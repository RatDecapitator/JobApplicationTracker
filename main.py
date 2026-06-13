from src.job_application import JobApplication
from src.job_application_manager import JobApplicationManager

manager = JobApplicationManager()

app1 = JobApplication(
    "Google",
    "Backend Developer",
    "Warsaw",
    "2025-06-12",
    "CV_v1",
)

app2 = JobApplication(
    "Microsoft",
    "Python Developer",
    "Krakow",
    "2025-06-13",
    "CV_v2",
)

app3 = JobApplication(
    "Amazon",
    "Software Engineer",
    "Remote",
    "2025-06-14",
    "CV_v1",
)

manager.add_application(app1)
manager.add_application(app2)
manager.add_application(app3)

print("=== ALL APPLICATIONS ===")
for application in manager.get_all_applications():
    print(application.id, application.company_name)

print("\n=== FIND APPLICATION ===")
found = manager.find_application(2)

if found:
    print(found.id, found.company_name)

print("\n=== REMOVE APPLICATION ===")
manager.remove_application(2)

for application in manager.get_all_applications():
    print(application.id, application.company_name)
