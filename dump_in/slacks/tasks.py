from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True)
def send_slack_for_exception_task(self, exc: str, context: str):
    from dump_in.slacks.services import SlackAPI

    try:
        slack_api = SlackAPI()
        slack_api.send_slack_for_exception(exc, context)

    except Exception as e:
        logger.warning(f"Exception occurred while sending slack message: {e}")
        self.retry(exc=e, countdown=5)
