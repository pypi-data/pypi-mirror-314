from typing import Optional, Any
from traceback import format_exc

from .types import (
    QueryType,
    HeadersType,
    GetHandlerType,
    PostHandlerType,
    ReturnType,
    ExceptionHandler,
)
from .exceptions import (
    ApiException,
    InternalServiceErrorException,
    MethodNotAllowedException,
)
from .logger import logger


def handle(
    method: str,
    query: QueryType,
    headers: HeadersType,
    body: Optional[Any] = None,
    get: Optional[GetHandlerType] = None,
    post: Optional[PostHandlerType] = None,
    handle_exception: Optional[ExceptionHandler] = None,
) -> ReturnType:
    try:
        if method == "POST" and post:
            return post(query, headers, body)
        elif method == "GET" and get:
            return get(query, headers)
    except ApiException as e:
        raise e
    except Exception as e:
        if handle_exception is not None:
            try:
                handle_exception(e)
            except:
                logger.exception(f"EXCEPTION HANDLER FAILED")
        else:
            logger.exception(f"UNEXPECTED EXCEPTION WHILE HANDLING REQUEST")
        raise InternalServiceErrorException()

    raise MethodNotAllowedException()
