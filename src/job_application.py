from src.application_status import ApplicationStatus


class JobApplication:

    def __init__(
        self,
        company_name,
        job_title,
        location,
        application_date,
        cv_used,
        id=None,
        status=ApplicationStatus.PENDING,
    ):
        self.company_name = company_name
        self.job_title = job_title
        self.location = location
        self.application_date = application_date
        self.cv_used = cv_used
        self.status = status
        self.id = id

        self.responses = []

    def change_status(self, new_status):
        self.status = new_status

    def add_response(self, response):
        self.responses.append(response)
