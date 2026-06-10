from src.response_type import ResponseType


class CompanyResponse:
    def __init__(self, response_date, content, response_type):
        self.response_date = response_date
        self.content = content
        self.response_type = response_type
