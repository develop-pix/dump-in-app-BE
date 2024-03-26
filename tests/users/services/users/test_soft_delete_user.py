import pytest

from dump_in.users.services.users import UserService

pytestmark = pytest.mark.django_db


class TestSoftDeleteUser:
    def setup_method(self):
        self.service = UserService()

    def test_soft_delete_user_success(self, group, user_social_provider, valid_user):
        user = self.service.soft_delete_user(
            user_id=valid_user.id,
        )

        valid_user.refresh_from_db()
        assert user.is_deleted == valid_user.is_deleted
        assert user.deleted_at == valid_user.deleted_at
