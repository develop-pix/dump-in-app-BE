from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command

logger = get_task_logger(__name__)


@shared_task(bind=True)
def flush_expired_tokens_task(self):
    call_command("flushexpiredtokens")
    logger.info("Successfully flushed expired tokens")
