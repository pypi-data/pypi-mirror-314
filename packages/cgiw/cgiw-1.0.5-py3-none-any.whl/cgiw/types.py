from typing import Callable, Dict, List, Any, Tuple, Optional, Union


QueryType = Dict[str, List[str]]
HeadersType = Dict[str, str]
ReturnType = Tuple[HeadersType, str]
GetHandlerType = Callable[[QueryType, HeadersType], ReturnType]
PostHandlerType = Callable[[QueryType, HeadersType, Any], ReturnType]
HandlerType = Union[GetHandlerType, PostHandlerType]
BodyWrapperType = Callable[[Any], Any]
HeadersWrapperType = Callable[[HeadersType], HeadersType]
ExceptionHandler = Callable[[Exception], None]

JsonType = Optional[Union[dict, list, int, float, str, bool]]
