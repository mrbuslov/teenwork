import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

app = Celery('website')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() # будет искать все задания в нашем проекте


app.conf.beat_schedule = { # расписание
    'deleting_24h': {
        'task': 'board.tasks.delete_24h',
        # https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html#crontab-schedules
        'schedule': crontab(minute=0, hour='*/24'),
    }
}

