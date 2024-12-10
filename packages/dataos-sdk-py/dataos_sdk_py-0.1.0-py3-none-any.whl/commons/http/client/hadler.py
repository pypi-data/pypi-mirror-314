from uplink import response_handler


class ApiException(Exception):
    """Base exception class for API-related errors."""


class InvalidRequestException(ApiException):
    """Exception raised for 400 Bad Request."""


class UnauthorizedException(ApiException):
    """Exception raised for 401 Unauthorized."""


class ForbiddenException(ApiException):
    """Exception raised for 403 Forbidden."""


class NotFoundException(ApiException):
    """Exception raised for 404 Not Found."""


# Define the decorator function
@response_handler
def raise_for_status_code(response):
    """Decorator to raise exceptions based on status code."""
    if response.status_code < 200 or response.status_code > 300:
        if response.status_code == 400:
            raise InvalidRequestException("Invalid request.", response.text)
        elif response.status_code == 401:
            raise UnauthorizedException("Unauthorized access.", response.text)
        elif response.status_code == 403:
            raise ForbiddenException("Access forbidden.", response.text)
        elif response.status_code == 404:
            raise NotFoundException("Resource not found.", response.text)
        else:
            raise Exception(f"status code {response.status_code, response.text}")
    return response
