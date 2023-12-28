import pytest

from dump_in.authentication.services.kakao_oauth import KakaoLoginFlowService
from dump_in.common.exception.exceptions import AuthenticationFailedException


class TestKakaoLoginFlow:
    def setup_method(self):
        self.service = KakaoLoginFlowService()

    def test_get_user_info_success(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        # @TODO 생년월일, 성별 추가 필요
        mock_response.text = """
        {
            "id": 123456789,
            "kakao_account": {
                "profile": {
                    "nickname": "test_nickname"
                },
                "email": "test_email"
            }
        }
        """
        mocker.patch("dump_in.authentication.services.kakao_oauth.requests.get", return_value=mock_response)
        access_token = "test_access_token"
        user_info = self.service.get_user_info(access_token)

        assert user_info["id"] == 123456789
        assert user_info["kakao_account"]["profile"]["nickname"] == "test_nickname"
        assert user_info["kakao_account"]["email"] == "test_email"

    def test_get_user_info_fail_response_not_200(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 401

        mocker.patch("dump_in.authentication.services.kakao_oauth.requests.get", return_value=mock_response)
        access_token = "test_access_token"
        with pytest.raises(AuthenticationFailedException) as e:
            self.service.get_user_info(access_token)

        assert e.value.detail == "Failed to get user info from Kakao."
        assert e.value.status_code == 401
