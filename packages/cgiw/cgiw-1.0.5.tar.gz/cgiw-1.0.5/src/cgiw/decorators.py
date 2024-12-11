from typing import Any, Callable, Optional, Type

#  IDK WHY PY.TYPED MARKER ISNT WORKING

from rtdce import enforce  # type: ignore


from .exceptions import BadRequestException
from .types import (
    PostHandlerType,
    BodyWrapperType,
    QueryType,
    HeadersType,
    ReturnType,
    HeadersWrapperType,
    HandlerType,
)


def wrap_body(
    process_body: BodyWrapperType,
) -> Callable[[PostHandlerType], PostHandlerType]:
    def wrap(post_handler: PostHandlerType) -> PostHandlerType:
        def wrapper(query: QueryType, headers: HeadersType, body: Any) -> ReturnType:
            return post_handler(query, headers, process_body(body))

        return wrapper

    return wrap


def wrap_headers(
    process_headers: HeadersWrapperType,
) -> Callable[[HandlerType], HandlerType]:
    def wrap(handler: HandlerType) -> HandlerType:
        def wrapper(
            query: QueryType, headers: HeadersType, *args, **kwargs
        ) -> ReturnType:
            return handler(query, process_headers(headers), *args, **kwargs)

        return wrapper

    return wrap


def create_type_validator(type_: Type):
    def validator(data: Any):
        if not isinstance(data, type_):
            raise BadRequestException(f"{data} is not type {type_}")
        return data

    return validator


def create_class_instantiator(class_: type):
    def instantiator(data: dict):
        try:
            return class_(**data)
        except TypeError:
            raise BadRequestException

    return instantiator


def enforce_dataclass(dataclass_instance):
    try:
        enforce(dataclass_instance)
    except TypeError as e:
        raise BadRequestException(message=str(e))
    return dataclass_instance
