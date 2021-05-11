import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_staff.settings")

app = Celery("company_staff")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'salary_accounting-2-hours': {
        'task': 'employees.tasks.salary_accounting',
        'schedule': crontab(minute=0, hour='*/2')
    }
}
