from enum import Enum


class RequestTypes(Enum):
    """Enums for request types"""

    OTP_REQUEST = "OTP_REQUEST"
    OTP_VERIFY = "OTP_VERIFY"
    EPFO_DETAILS = "EPFO_DETAILS"
