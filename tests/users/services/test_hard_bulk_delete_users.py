import pytest

from dump_in.users.models import User
from dump_in.users.services import UserService

pytestmark = pytest.mark.django_db


class TestHardBulkDeleteUsers:
    def setup_method(self):
        self.service = UserService()

    def test_hard_delete_user_success(self, group, user_social_provider, deleted_user):
        self.service.hard_bulk_delete_users(days=14)
        assert User.objects.filter(id=deleted_user.id).exists() is False
