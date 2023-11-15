import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from dump_in.slacks.services import SlackAPI, slack_api_get_config


def test_send_slack_for_exception_success(mocker):
    mock_instance = mocker.Mock()
    mocker.patch("django.conf.settings.SLACK_API_TOKEN", "your_test_token")
    mocker.patch("django.conf.settings.SLACK_ERROR_CHANNEL_ID", "your_test_channel_id")
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


def test_slack_api_get_config_success(mocker):
    mocker.patch("django.conf.settings.SLACK_API_TOKEN", "your_test_token")
    mocker.patch("django.conf.settings.SLACK_ERROR_CHANNEL_ID", "your_test_channel_id")

    configs = slack_api_get_config()

    assert configs.token == "your_test_token"
    assert configs.error_channel_id == "your_test_channel_id"


def test_slack_api_get_config_fail_missing_token(mocker):
    mocker.patch("django.conf.settings.SLACK_API_TOKEN", None)
    mocker.patch("django.conf.settings.SLACK_ERROR_CHANNEL_ID", "your_test_channel_id")

    with pytest.raises(ImproperlyConfigured):
        slack_api_get_config()


def test_slack_api_get_config_fail_missing_channel_id(mocker):
    mocker.patch("django.conf.settings.SLACK_API_TOKEN", "your_test_token")
    mocker.patch("django.conf.settings.SLACK_ERROR_CHANNEL_ID", None)

    with pytest.raises(ImproperlyConfigured):
        slack_api_get_config()
