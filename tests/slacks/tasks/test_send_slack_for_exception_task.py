from unittest.mock import MagicMock, patch

from django.test import TestCase

from dump_in.slacks.tasks import send_slack_for_exception_task


class SendSlackForExceptionTaskTests(TestCase):
    @patch("dump_in.slacks.services.SlackAPI")
    def test_send_slack_for_exception_task_success(self, mock_slack_api):
        mock_slack_instance = mock_slack_api.return_value
        mock_slack_instance.send_slack_for_exception = MagicMock()

        send_slack_for_exception_task(exc="TestException", context="TestContext")

        self.assertTrue(mock_slack_instance.send_slack_for_exception.called)

    @patch("dump_in.slacks.services.SlackAPI")
    def test_send_slack_for_exception_task_retry_success(self, mock_slack_api):
        mock_slack_instance = mock_slack_api.return_value
        mock_slack_instance.send_slack_for_exception = MagicMock(side_effect=Exception)

        with self.assertRaises(Exception):
            send_slack_for_exception_task(exc="TestException", context="TestContext")

        self.assertTrue(mock_slack_instance.send_slack_for_exception.called)
