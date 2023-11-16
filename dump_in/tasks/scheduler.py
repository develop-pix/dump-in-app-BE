from celery.schedules import crontab

from dump_in.tasks.celery import app

app.conf.beat_schedule = {
    "flush_expired_tokens": {
        "task": "dump_in.authentication.tasks.flush_expired_tokens_task",
        "schedule": crontab(minute="0", hour="4"),
    },
}
