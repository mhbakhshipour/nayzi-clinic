from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class CustomAPIException(APIException):
    def __init__(self, detail=None, code=None):
        super().__init__(detail=detail, code=code)
        if code:
            self.code = code


def custom_rest_exception_handler(exc, context):
    if isinstance(exc, APIException):
        response = exception_handler(exc, context)
        if hasattr(exc, 'code'):
            response.data = {'status': 'error', 'data': exc.detail, 'code': exc.code}
        else:
            response.data = {'status': 'error', 'data': exc.detail}
        return response


class HttpBadRequestException(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST


class HttpNotFoundException(CustomAPIException):
    status_code = status.HTTP_404_NOT_FOUND


class HttpUnauthorizedException(CustomAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED


class HttpUnProcessableEntityException(CustomAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class HttpConflictException(CustomAPIException):
    status_code = status.HTTP_409_CONFLICT


class HttpPreconditionFailedException(CustomAPIException):
    status_code = status.HTTP_412_PRECONDITION_FAILED


class HttpServiceUnavailableException(CustomAPIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class HttpInternalServerException(CustomAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
