from enum import Enum


class ApplicationStatus(Enum):
    PENDING = "Pending"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAW = "Withdraw"
