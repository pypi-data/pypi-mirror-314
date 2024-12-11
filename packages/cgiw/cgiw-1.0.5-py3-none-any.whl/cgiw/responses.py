from json import dumps
from typing import Optional, Union, Tuple, Dict
from urllib.parse import urlencode

from .types import JsonType, ReturnType, QueryType


def json(obj: JsonType) -> ReturnType:
    return ({"Status": "200 OK", "Content-Type": "application/json"}, dumps(obj))


def redirect(url: str, query: Optional[QueryType] = None) -> ReturnType:
    if query:
        url += f"?{urlencode(query)}"
    headers = {
        "Status": "301 Moved Permanently",
        "Location": url,
        "Content-Type": "text/plain",
    }
    return (headers, f"Redirecting to {url}...")
