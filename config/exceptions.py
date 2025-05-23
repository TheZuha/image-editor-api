from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.response import Response
import logging

logger = logging.getLogger('django')

class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A server error occurred.'
    default_code = 'error'

    def __init__(self, detail=None, code=None, status_code=None):
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail, code)

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Log the error
        logger.error(f"Error occurred: {exc.__class__.__name__} - {str(exc)}")
        
        # Add custom error format
        error_data = {
            'error': {
                'code': response.status_code,
                'message': response.data.get('detail', str(response.data)),
                'type': exc.__class__.__name__
            }
        }
        response.data = error_data

    return response 