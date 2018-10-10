celery -A app.celery worker --pool=solo -l info
python app.py