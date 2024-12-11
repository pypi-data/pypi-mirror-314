from unittest import TestCase, mock
from os import environ
from io import StringIO
from random import randint

from src.cgiw.parsers import parse_query, parse_headers, parse_body
from src.cgiw import parsers


class TestParsers(TestCase):
    @mock.patch.dict(environ, {"QUERY_STRING": "hello=world&test=123"})
    def test_parse_query(self):
        result = parse_query()
        self.assertEqual(result, {"hello": ["world"], "test": ["123"]})

    @mock.patch.dict(environ, {"CONTENT_TYPE": "text/plain", "CONTENT_LENGTH": "11"})
    def test_parse_headers(self):
        result = parse_headers()
        self.assertEqual(result, {"Content-Type": "text/plain", "Content-Length": "11"})

    def test_parse_body(self):
        body = str(randint(111, 999999))
        headers = {"Content-Length": str(len(body))}
        parsers.stdin = StringIO(body)
        result = parse_body(headers)
        self.assertEqual(result, body)
