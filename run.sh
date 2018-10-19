celery -A app.celery worker --pool=solo -l info
python app.py

CELERY_BROKER_URL = 'amqp://localhost//