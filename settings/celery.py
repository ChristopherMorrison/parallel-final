import os

import django
from celery import Celery

from settings import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()
app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(settings.INSTALLED_APPS, force=True)


@app.task(bind=True)
def celery_check(self):
    print('It works')
