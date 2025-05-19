from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


def custom_exception_handler(exc, context):
    """Кастомный обработчик исключений"""
    response = exception_handler(exc, context)

    if isinstance(exc, (DatabaseError, TimeoutError)):
        return Response(
            {
                "error": "Service Unavailable",
                "detail": str(exc),
                "code": "service_unavailable"
            },
            status=503
        )

    return response
