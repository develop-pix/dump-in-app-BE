from celery import shared_task
from celery.utils.log import get_task_logger

from dump_in.users.services.users import UserService

logger = get_task_logger(__name__)


@shared_task(bind=True)
def hard_delete_users_task(self):
    try:
        user_service = UserService()
        user_service.hard_bulk_delete_users(days=14)
        logger.info("Successfully hard deleted users")

    except Exception as e:
        logger.warning(f"Hard delete users task failed: {e}")
        self.retry(exc=e, countdown=60)
