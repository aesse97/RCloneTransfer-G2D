import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rclonefun.settings')

app = Celery('rclonefun')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'amqp://localhost'

app.autodiscover_tasks()