from unittest import TestCase, mock
from os import environ

from src.cgiw.run import run
from src.cgiw.exceptions import ApiException


class TestRun(TestCase):
    @mock.patch.dict(environ, {"REQUEST_METHOD": "GET"})
    def test_run_get(self):
        def handler(query, headers):
            return ({}, "")

        result = run(get=handler)
        self.assertEqual(result, "\n\n")

    @mock.patch.dict(environ, {"REQUEST_METHOD": "POST"})
    def test_run_post(self):
        def handler(query, headers, body):
            return ({}, "")

        result = run(post=handler)
        self.assertEqual(result, "\n\n")

    @mock.patch.dict(environ, {"REQUEST_METHOD": "GET"})
    def test_run_exception(self):
        code = 404
        status_text = "Not Found"
        message = "Resource Not Found"

        def handler(query, headers):
            raise ApiException(code, status_text, message=message)

        result = run(get=handler)
        self.assertEqual(result, f"Status: {code} {status_text}\n\n{message}")
