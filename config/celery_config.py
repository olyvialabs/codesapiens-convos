import os
from config.settings import settings
broker_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
result_backend = os.environ.get('REDIS_URL', 'redis://localhost:6379/1')

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
