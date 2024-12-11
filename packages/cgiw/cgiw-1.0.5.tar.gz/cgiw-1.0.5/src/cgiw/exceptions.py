from typing import Optional


class ApiException(Exception):
    def __init__(self, code: int, status_text: str, message: Optional[str] = None):
        self.code = code
        self.status_text = status_text
        self.message = message or status_text

        super().__init__(f"Status {self.code} {self.status_text}: {self.message}")

    def compose(self):
        return ({"Status": f"{self.code} {self.status_text}"}, self.message)


class BadRequestException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(400, "Bad Request", message=message)


class UnauthorizedException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(401, "Unauthorized", message=message)


class PaymentRequiredException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(402, "Payment Required", message=message)


class ForbiddenException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(403, "Forbidden", message=message)


class NotFoundException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(404, "Not Found", message=message)


class MethodNotAllowedException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(405, "Method Not Allowed", message=message)


class NotAcceptableException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(406, "Not Acceptable", message=message)


class ProxyAuthenticationRequiredException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(407, "Proxy Authentication Required", message=message)


class RequestTimeoutException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(408, "Request Timeout", message=message)


class ConflictException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(409, "Conflict", message=message)


class GoneException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(410, "Gone", message=message)


class LengthRequiredException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(411, "Length Required", message=message)


class PreconditionException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(412, "Precondition Failed", message=message)


class PayloadTooLargeException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(413, "Payload Too Large", message=message)


class URITooLongException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(414, "URI Too Long", message=message)


class UnsupportedMediaTypeException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(415, "Unsupported Media Type", message=message)


class RangeNotSatisfiableException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(416, "Range Not Satisfiable", message=message)


class ExpectationFailedException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(417, "Expectation Failed", message=message)


class ImATeaPotException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(418, "I'm a Teapot", message=message)


class MisdirectedRequestException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(421, "Misdirected Request", message=message)


class UnprocessableContentException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(422, "Unprocessable Content", message=message)


class LockedException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(423, "Locked", message=message)


class FailedDependencyException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(424, "Failed Dependency", message=message)


class TooEarlyException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(425, "Too Early", message=message)


class UpgradeRequiredException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(426, "Upgrade Required", message=message)


class PreconditionRequiredException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(428, "Precondition Required", message=message)


class TooManyRequestsException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(429, "Too Many Requests", message=message)


class RequestHeaderFieldsTooLargeException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(431, "Request Header Fields Too Large", message=message)


class UnavailableForLegalReasonsException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(451, "Unavailable For Legal Reasons", message=message)


class InternalServiceErrorException(ApiException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(500, "Internal Service Error", message=message)
