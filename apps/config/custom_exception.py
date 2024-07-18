from rest_framework import status
from rest_framework.exceptions import APIException

class DomainException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {"message": "도메인 로직상 문제 발생..."}
    default_code = "invalid"