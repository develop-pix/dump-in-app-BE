import pytest
from celery.result import EagerResult

from dump_in.users.tasks import hard_delete_users_task

pytestmark = pytest.mark.django_db


def test_hard_delete_users_task_success():
    result: EagerResult = hard_delete_users_task.apply()

    assert result.successful()


def test_hard_delete_users_task_fail_exception(mocker):
    mocker.patch("dump_in.users.tasks.UserService", side_effect=Exception("test"))
    result: EagerResult = hard_delete_users_task.apply()

    assert not result.successful()
