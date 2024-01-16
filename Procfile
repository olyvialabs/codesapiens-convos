web: gunicorn app:app
worker: celery -A background_jobs worker -l INFO --loglevel=INFO --concurrency 1