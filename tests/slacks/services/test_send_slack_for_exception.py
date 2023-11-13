from unittest.mock import MagicMock, patch

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from dump_in.slacks.services import SlackAPI, slack_api_get_config


class SendSlackForExceptionTests(TestCase):
    def setUp(self):
        self.original_slack_api_token = getattr(settings, "SLACK_API_TOKEN", None)
        self.original_slack_error_channel_id = getattr(settings, "SLACK_ERROR_CHANNEL_ID", None)
        settings.SLACK_API_TOKEN = "your_test_token"
        settings.SLACK_ERROR_CHANNEL_ID = "your_test_channel_id"

    def tearDown(self):
        settings.SLACK_API_TOKEN = self.original_slack_api_token
        settings.SLACK_ERROR_CHANNEL_ID = self.original_slack_error_channel_id

    @patch("dump_in.slacks.services.WebClient")
    def test_send_slack_for_exception_success(self, mock_web_client):
        mock_instance = mock_web_client.return_value
        mock_instance.chat_postMessage = MagicMock()

        slack_api_instance = SlackAPI()

        slack_api_instance.send_slack_for_exception("TestException", "TestContext")

        mock_instance.chat_postMessage.assert_called_once_with(
            channel=settings.SLACK_ERROR_CHANNEL_ID,
            attachments=[
                {
                    "title": "에러 발생 :bug:",
                    "text": "Exception(예외처리 종류), Context(에러 상세내용)를 확인하세요.",
                    "color": "#FF0000",
                    "fields": [
                        {
                            "title": "Exception",
                            "value": "TestException",
                            "short": True,
                        },
                        {
                            "title": "Context",
                            "value": "TestContext",
                            "short": True,
                        },
                    ],
                }
            ],
        )

    def test_slack_api_get_config_success(self):
        settings.SLACK_API_TOKEN = "your_test_token"
        settings.SLACK_ERROR_CHANNEL_ID = "your_test_channel_id"

        configs = slack_api_get_config()

        self.assertEqual(configs.token, "your_test_token")
        self.assertEqual(configs.error_channel_id, "your_test_channel_id")

    def test_slack_api_get_config_fail_missing_token(self):
        settings.SLACK_API_TOKEN = None
        settings.SLACK_ERROR_CHANNEL_ID = "your_test_channel_id"

        with self.assertRaises(ImproperlyConfigured):
            slack_api_get_config()

    def test_slack_api_get_config_fail_missing_channel_id(self):
        settings.SLACK_API_TOKEN = "your_test_token"
        settings.SLACK_ERROR_CHANNEL_ID = None

        with self.assertRaises(ImproperlyConfigured):
            slack_api_get_config()
