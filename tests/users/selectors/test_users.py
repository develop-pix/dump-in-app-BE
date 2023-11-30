from dump_in.users.selectors.users import UserSelector


class TestUserSelector:
    def setup_method(self):
        self.user_selector = UserSelector()

    def test_get_user_by_id_success(self, new_users):
        user_id = 1
        user_email = "test1@test.com"

        user = self.user_selector.get_user_by_id(user_id)

        assert user.id == user_id
        assert user.email == user_email

    def test_get_user_by_id_fail_does_not_exist(self, new_users):
        user_id = 20
        user = self.user_selector.get_user_by_id(user_id)
        assert user is None

    def test_get_user_by_username_for_auth_success(self, new_users):
        user_id = 1
        username = "test1"
        user_email = "test1@test.com"

        user = self.user_selector.get_user_by_username_for_auth(username)

        assert user.id == user_id
        assert user.username == username
        assert user.email == user_email

    def test_get_user_by_username_for_auth_fail_does_not_exist(self, new_users):
        user_id = 20
        user = self.user_selector.get_user_by_username_for_auth(user_id)
        assert user is None

    def test_get_user_by_username_success(self, new_users):
        user_id = 1
        username = "test1"
        user_email = "test1@test.com"

        user = self.user_selector.get_user_by_username(username)

        assert user.id == user_id
        assert user.username == username
        assert user.email == user_email

    def test_get_user_by_username_fail_does_not_exist(self, new_users):
        username = "test12"
        user = self.user_selector.get_user_by_username(username)
        assert user is None

    def test_check_is_exists_user_by_nickname_success(self, new_users):
        nickname = "test1"
        is_exists = self.user_selector.check_is_exists_user_by_nickname(nickname)
        assert is_exists is True

    def test_get_user_queryset_by_delated_at_lte_days_success(self, deleted_users):
        users = self.user_selector.get_user_queryset_by_delated_at_lte_days(days=10)

        assert users.count() == 1
        assert users[0].is_deleted is True
        assert users[0].deleted_at is not None
