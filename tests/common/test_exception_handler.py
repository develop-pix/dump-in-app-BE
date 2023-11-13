from django.test import TestCase
from rest_framework.exceptions import APIException

from dump_in.common.exception.exception_handler import (
    default_exception_handler,
    handle_api_exception,
)


class ExceptionHandlerTest(TestCase):
    def test_handle_api_exception(self):
        api_exception = APIException(detail="Test exception", code=1000)

        response = handle_api_exception(api_exception, {})

        self.assertEqual(response.data["code"], 1000)
        self.assertEqual(response.data["message"], "Test exception")
        self.assertEqual(response.status_code, 500)

    def test_default_exception_handler(self):
        exception = Exception("Test exception")

        response = default_exception_handler(exception, {})

        self.assertEqual(response.status_code, 500)
