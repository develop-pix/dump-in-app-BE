from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command

logger = get_task_logger(__name__)


@shared_task(bind=True)
def flush_expired_tokens_task(self):
    try:
        call_command("flushexpiredtokens")
        logger.info("Successfully flushed expired tokens")

    except Exception as e:
        logger.warning(f"Exception occurred while flushing expired tokens: {e}")
        self.retry(exc=e, countdown=5)
