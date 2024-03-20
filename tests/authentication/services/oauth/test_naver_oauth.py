import pytest

from dump_in.authentication.services.naver_oauth import NaverLoginFlowService
from dump_in.common.exception.exceptions import AuthenticationFailedException


class TestNaverLoginFlow:
    def setup_method(self):
        self.naver_login_flow_service = NaverLoginFlowService()

    def test_get_user_info_success(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = """
        {
            "response": {
                "id": 123456789,
                "nickname": "test_nickname",
                "email": "test_email@test.com",
                "gender": "F",
                "birthyear": "2023",
                "birthday": "01-01"
                }
        }
        """
        mocker.patch("dump_in.authentication.services.naver_oauth.requests.get", return_value=mock_response)
        access_token = "test_access_token"
        user_info = self.naver_login_flow_service.get_user_info(access_token)

        assert user_info["id"] == 123456789
        assert user_info["nickname"] == "test_nickname"
        assert user_info["email"] == "test_email@test.com"
        assert user_info["gender"] == "F"
        assert user_info["birthyear"] == "2023"
        assert user_info["birthday"] == "01-01"

    def test_get_user_info_fail_response_not_200(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 401

        mocker.patch("dump_in.authentication.services.naver_oauth.requests.get", return_value=mock_response)
        access_token = "test_access_token"
        with pytest.raises(AuthenticationFailedException) as e:
            self.naver_login_flow_service.get_user_info(access_token)

        assert e.value.detail == "Failed to get user info from Naver."
        assert e.value.status_code == 401
