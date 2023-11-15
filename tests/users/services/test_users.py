import pytest

from dump_in.common.constants import USER_SOCIAL_PROVIDER_KAKAO
from dump_in.users.services.users import UserService

pytestmark = pytest.mark.django_db


class TestUserService:
    def setup_method(self):
        self.service = UserService()

    def test_get_or_create_social_user_success(self, group, user_social_provider):
        user = self.service.get_or_create_social_user(
            email="test@test.com",
            nickname="test_nickname",
            social_id="test_social_id",
            birth="20230101",
            gender="female",
            social_provider=USER_SOCIAL_PROVIDER_KAKAO,
        )
        assert user.email == "test@test.com"
        assert user.nickname == "test_nickname"
        assert user.username == "test_social_id"
        assert user.birth.strftime("%Y%m%d") == "20230101"
        assert user.gender == "F"
        assert user.user_social_provider.id == USER_SOCIAL_PROVIDER_KAKAO
