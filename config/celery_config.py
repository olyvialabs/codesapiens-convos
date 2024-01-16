import os
from config.settings import settings
broker_url = os.environ.get('REDIS_URL', settings.CELERY_BROKER_URL)
result_backend = os.environ.get('REDIS_URL', settings.CELERY_RESULT_BACKEND)

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
