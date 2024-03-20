import pytest

from dump_in.authentication.services.apple_oauth import AppleLoginFlowService
from dump_in.common.exception.exceptions import AuthenticationFailedException


class TestAppleLoginFlow:
    def setup_method(self):
        self.apple_login_flow_service = AppleLoginFlowService()

    def test_get_user_info_success(self):
        identify_token = (
            "eyJraWQiOiJmaDZCczhDIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL2FwcGx"
            "laWQuYXBwbGUuY29tIiwiYXVkIjoic3RyaW5nIiwiZXhwIjoxNzA0MDEzNjY3LCJpYXQiO"
            "jE3MDM5MjcyNjcsInN1YiI6InN0cmluZyIsIm5vbmNlIjoic3RyaW5nIiwiY19oYXNoIjo"
            "ic3RyaW5nIiwiZW1haWwiOiJzdHJpbmdAc3RyaW5nLmNvbSIsImVtYWlsX3ZlcmlmaWVkIj"
            "oidHJ1ZSIsImF1dGhfdGltZSI6MTcwMzkyNzI2Nywibm9uY2Vfc3VwcG9ydGVkIjp0cnVlL"
            "CJyZWFsX3VzZXJfc3RhdHVzIjoyfQ.Y_ojDrw0N-_Sv3Ld4TwyuqzCYlQtkbj8uCKB13BeDy"
            "ZjNmXhdCYZKa9dQLKE3zStm-F1vuA18cqBuuicrWdsEwKLHDTIY34-FiNu3L0oqEIRzI6hF--"
            "CgnN5o3FNCCpHTaESD942GoFgn0B3ip-0512kaEfHVkm8t62Mikb4jJAqZx95fz4zHujtKZfVL"
            "jHDFBg3nKlZ0az94LrUi8PYqsKxwG-2Sh72NQeZJVdtws5cckc6gQBmKVlanz5YCkiE4NipaHlY"
            "Bc5N8Hn_ShxaQZqwAqIu3ROlkue71ywvhXUU_rxjJf7Gs4dzHZd7LdOds6VZdRpcctW8g58CcXT5LA"
        )
        user_info = self.apple_login_flow_service.get_user_info(identify_token)

        assert user_info["iss"] == "https://appleid.apple.com"
        assert user_info["aud"] == "string"
        assert user_info["exp"] == 1704013667
        assert user_info["iat"] == 1703927267
        assert user_info["sub"] == "string"
        assert user_info["nonce"] == "string"
        assert user_info["c_hash"] == "string"
        assert user_info["email"] == "string@string.com"
        assert user_info["email_verified"] == "true"
        assert user_info["auth_time"] == 1703927267
        assert user_info["nonce_supported"] is True
        assert user_info["real_user_status"] == 2

    def test_get_user_info_fail_invalid_token(self):
        identify_token = "wrong_token"
        with pytest.raises(AuthenticationFailedException) as e:
            self.apple_login_flow_service.get_user_info(identify_token)

        assert str(e.value) == "Token is invalid"
        assert isinstance(e.value, AuthenticationFailedException)
