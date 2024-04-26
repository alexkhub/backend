import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
# response = app.control.enable_events(reply=True)

app.conf.beat_schedule = {
    'order_deadline': {
            'task': 'core.tasks.order_deadline',
            'schedule': crontab(minute='*/2', )
        },
    'employee_rating' : {
            'task': 'core.tasks.employee_rating',
            'schedule': crontab(minute='*/1', )
    }

}