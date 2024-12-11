from os import getenv
from typing import Optional

from .types import ExceptionHandler, GetHandlerType, PostHandlerType
from .parsers import parse_query, parse_headers, parse_body
from .handler import handle
from .composers import compose_response
from .exceptions import ApiException
from .logger import logger


def run(
    get: Optional[GetHandlerType] = None,
    post: Optional[PostHandlerType] = None,
    handle_exception: Optional[ExceptionHandler] = None,
):
    method = getenv("REQUEST_METHOD", "")
    query = parse_query()
    headers = parse_headers()
    body = parse_body(headers)
    try:
        response = handle(
            method,
            query,
            headers,
            body,
            get=get,
            post=post,
            handle_exception=handle_exception,
        )
    except ApiException as e:
        response = e.compose()
    result = compose_response(*response)
    print(result)
    return result
