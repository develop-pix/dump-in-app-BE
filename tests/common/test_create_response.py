from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from dump_in.common.response import create_response


class CreateResponseTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_response(self):
        data = {"key": "value"}
        code = 0
        message = "Test successful"
        status_code = status.HTTP_201_CREATED

        response = create_response(data=data, code=code, message=message, status_code=status_code)

        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.data["code"], code)
        self.assertEqual(response.data["message"], message)
        self.assertEqual(response.data["data"], data)
        self.assertTrue(response.data["success"])
