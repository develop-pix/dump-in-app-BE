import pytest

from dump_in.slacks.tasks import send_slack_for_exception_task


def test_send_slack_for_exception_task_success(mocker):
    mock_instance = mocker.Mock()
    mocker.patch("dump_in.slacks.services.SlackAPI", return_value=mock_instance)
    send_slack_for_exception_task(exc="TestException", context="TestContext")

    assert mock_instance.send_slack_for_exception.called


def test_send_slack_for_exception_task_with_exception(mocker):
    mock_instance = mocker.Mock()
    mocker.patch("dump_in.slacks.services.SlackAPI", return_value=mock_instance)
    mocker.patch.object(mock_instance, "send_slack_for_exception", side_effect=Exception("Mocked exception"))

    with pytest.raises(Exception, match="Mocked exception"):
        send_slack_for_exception_task(exc="TestException", context="TestContext")

    assert mock_instance.send_slack_for_exception.called
