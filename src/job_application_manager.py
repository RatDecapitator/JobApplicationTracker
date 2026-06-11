class JobApplicationManager:
    def __init__(self):
        self.applications = []
        self.next_id = 1

    def add_application(
        self,
        application,
    ):
        application.id = self.next_id
        self.applications.append(application)
        self.next_id += 1

    def get_all_applications(self):
        return self.applications

    def find_application(self, application_id):
        for application in self.applications:
            if application.id == application_id:
                return application

        return None
