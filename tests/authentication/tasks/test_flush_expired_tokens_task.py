import pytest
from celery.result import EagerResult

from dump_in.authentication.tasks import flush_expired_tokens_task

pytestmark = pytest.mark.django_db


def test_flush_expired_tokens_task_success():
    result: EagerResult = flush_expired_tokens_task.apply()
    assert result.successful()
