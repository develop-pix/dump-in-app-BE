from attr import define
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from slack import WebClient


@define
class SlackAPIConfigs:
    token: str
    error_channel_id: str


class SlackAPI:
    """
    슬랙 API 핸들러 클래스입니다.
    """

    def __init__(self):
        self.configs = slack_api_get_config()
        self.client = WebClient(token=self.configs.token)

    def send_slack_for_exception(self, exc: str, context: str):
        """
        예외 처리 중 UnkownServerException이 발생한 경우 슬랙으로 알림을 전송합니다.
        """
        self.client.chat_postMessage(
            channel=self.configs.error_channel_id,
            attachments=[
                {
                    "title": "에러 발생 :bug:",
                    "text": "Exception(예외처리 종류), Context(에러 상세내용)를 확인하세요.",
                    "color": "#FF0000",
                    "fields": [
                        {
                            "title": "Exception",
                            "value": exc,
                            "short": True,
                        },
                        {
                            "title": "Context",
                            "value": context,
                            "short": True,
                        },
                    ],
                }
            ],
        )


def slack_api_get_config() -> SlackAPIConfigs:
    token = settings.SLACK_API_TOKEN
    error_channel_id = settings.SLACK_ERROR_CHANNEL_ID

    if not token:
        raise ImproperlyConfigured("SLACK_API_TOKEN is not set.")

    if not error_channel_id:
        raise ImproperlyConfigured("SLACK_ERROR_CHANNEL_ID is not set.")

    configs = SlackAPIConfigs(token=token, error_channel_id=error_channel_id)
    return configs
