from unittest import TestCase
from urllib.parse import parse_qs
from json import loads, dumps
from random import randint

from src.cgiw.decorators import (
    wrap_body,
    wrap_headers,
    create_type_validator,
    create_class_instantiator,
)
from src.cgiw.exceptions import BadRequestException


class TestDecorators(TestCase):
    def test_wrap_body_qs(self):
        @wrap_body(parse_qs)
        def post_handler(query, headers, body):
            assert isinstance(body, dict)
            return ({}, "")

        post_handler({}, {}, "hello=world")

    def test_wrap_body_json(self):
        @wrap_body(loads)
        def post_handler(query, headers, body):
            assert isinstance(body, dict)
            return ({}, "")

        post_handler({}, {}, dumps({"hello": "world"}))

    def test_wrap_headers(self):
        user_id = str(randint(11111, 999999))

        def example(headers):
            return {**headers, "user": user_id}

        @wrap_headers(example)
        def handler(query, headers):
            assert headers["user"] == user_id
            return ({}, "")

        handler({}, {"Authorization": "eee"})

    def test_create_type_validator(self):
        validator = create_type_validator(int)

        self.assertRaises(BadRequestException, validator, "test")

        assert 123 == validator(123)

    def test_create_class_instantiator(self):
        class Test:
            pass

        instantiator = create_class_instantiator(Test)
        assert isinstance(instantiator({}), Test)

    def test_create_class_instantiator_type_error(self):
        class Test:
            pass

        instantiator = create_class_instantiator(Test)
        self.assertRaises(BadRequestException, instantiator, {"x": 123})