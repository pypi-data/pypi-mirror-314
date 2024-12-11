from unittest import TestCase
from random import randint

from src.cgiw.handler import handle


class TestHandler(TestCase):
    def test_handle_get(self):
        data = str(randint(111, 99999))

        method = "GET"
        query = {"data": [data]}

        def handler(query, headers):
            return ("200 OK", {"Content-Type": "text/plain"}, query["data"][0])

        result = handle(method, query, {}, get=handler)
        self.assertEqual(result, ("200 OK", {"Content-Type": "text/plain"}, data))

    def test_handle_post(self):
        data = str(randint(111, 99999))

        method = "POST"

        def handler(query, headers, body):
            return ("200 OK", {"Content-Type": "text/plain"}, body)

        result = handle(method, {}, {}, body=data, post=handler)
        self.assertEqual(result, ("200 OK", {"Content-Type": "text/plain"}, data))
