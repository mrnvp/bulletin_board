import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bboard.settings')
app = Celery('bboard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_sunday_3pm': {
        'task': 'bulletin.tasks.action_every_sunday_3pm',
        'schedule': crontab(hour=15, minute=00, day_of_week='sunday'),
    },
}


