import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from dump_in.slacks.services import SlackAPI, slack_api_get_config


class TestSlackAPI:
    def test_send_slack_for_exception_success(self, mocker):
        mock_instance = mocker.Mock()
        mocker.patch("dump_in.slacks.services.WebClient", return_value=mock_instance)

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

        assert slack_api_instance.configs.token == settings.SLACK_API_TOKEN
        assert slack_api_instance.configs.error_channel_id == settings.SLACK_ERROR_CHANNEL_ID
        assert mock_instance.chat_postMessage.called is True

    def test_slack_api_get_config_success(self):
        configs = slack_api_get_config()

        assert configs.token == settings.SLACK_API_TOKEN
        assert configs.error_channel_id == settings.SLACK_ERROR_CHANNEL_ID

    @override_settings(SLACK_API_TOKEN=None)
    def test_slack_api_get_config_fail_missing_token(self):
        with pytest.raises(ImproperlyConfigured) as e:
            slack_api_get_config()

        assert e.value.args[0] == "SLACK_API_TOKEN is not set."

    @override_settings(SLACK_ERROR_CHANNEL_ID=None)
    def test_slack_api_get_config_fail_missing_channel_id(self):
        with pytest.raises(ImproperlyConfigured) as e:
            slack_api_get_config()

        assert e.value.args[0] == "SLACK_ERROR_CHANNEL_ID is not set."
