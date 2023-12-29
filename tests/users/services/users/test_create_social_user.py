import pytest
from requests.models import Response

from dump_in.users.enums import UserProvider
from dump_in.users.services.users import UserService

pytestmark = pytest.mark.django_db


class TestCreateSocialUser:
    def setup_method(self):
        self.service = UserService()

    def test_create_social_user_success(self, group, user_social_provider, valid_user_mobile_token):
        user = self.service.create_social_user(
            email="test@test.com",
            nickname="test_nickname",
            social_id="test_social_id",
            birth="2023-01-01",
            gender="F",
            social_provider=UserProvider.KAKAO.value,
            mobile_token=valid_user_mobile_token.token,
        )

        assert user.email == "test@test.com"
        assert user.nickname == "test_nickname"
        assert user.username == "test_social_id"
        assert user.gender == "F"
        assert user.birth == "2023-01-01"
        assert user.mobile_tokens.first().user_id == user.id
        assert user.mobile_tokens.first().token == valid_user_mobile_token.token
        assert user.user_social_provider.id == UserProvider.KAKAO.value

    def test_create_social_user_success_nickname_exists(self, group, user_social_provider, valid_user_mobile_token, valid_user, mocker):
        mock_response = Response()
        mock_response.status_code = 200
        mock_response.json = mocker.Mock(return_value={"words": ["mocked_nickname"]})

        mocker.patch("dump_in.users.services.users.requests.get", return_value=mock_response)

        user = self.service.create_social_user(
            email="test@test.com",
            nickname=valid_user.nickname,
            social_id="test_social_id",
            birth="2023-01-01",
            gender="F",
            social_provider=UserProvider.KAKAO.value,
            mobile_token=valid_user_mobile_token.token,
        )

        assert user.email == "test@test.com"
        assert user.nickname != valid_user.nickname
        assert user.username == "test_social_id"
        assert user.gender == "F"
        assert user.birth == "2023-01-01"
        assert user.mobile_tokens.first().user_id == user.id
        assert user.mobile_tokens.first().token == valid_user_mobile_token.token
        assert user.user_social_provider.id == UserProvider.KAKAO.value

    def test_create_social_user_success_user_already_exists(self, valid_user):
        user = self.service.create_social_user(
            email=valid_user.email,
            nickname=valid_user.nickname,
            social_id=valid_user.username,
            birth=valid_user.birth,
            gender=valid_user.gender,
            social_provider=UserProvider.KAKAO.value,
            mobile_token="test_mobile_token",
        )

        assert user.email == valid_user.email
        assert user.nickname == valid_user.nickname
        assert user.username == valid_user.username
        assert user.gender == valid_user.gender
        assert user.birth == valid_user.birth

    def test_create_social_user_success_mobile_token_none(self, group, user_social_provider, valid_user, mocker):
        mock_response = Response()
        mock_response.status_code = 200
        mock_response.json = mocker.Mock(return_value={"words": ["mocked_nickname"]})

        mocker.patch("dump_in.users.services.users.requests.get", return_value=mock_response)

        user = self.service.create_social_user(
            email="test@test.com",
            nickname=valid_user.nickname,
            social_id="test_social_id",
            birth="2023-01-01",
            gender="F",
            social_provider=UserProvider.KAKAO.value,
            mobile_token=None,
        )

        assert user.email == "test@test.com"
        assert user.nickname != valid_user.nickname
        assert user.username == "test_social_id"
        assert user.gender == "F"
        assert user.birth == "2023-01-01"
        assert user.mobile_tokens.first() is None
