# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Exe file to Run"
"""
from celery.schedules import crontab

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "ds259802.mlab.com",
    "port": 59802,
    "database": "aldrin",
    "taskmeta_collection": "stock_taskmeta_collection",
}

#used to schedule tasks periodically and passing optional arguments
#Can be very useful. Celery does not seem to support scheduled task but only periodic
CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'tasks.add',
        'schedule': crontab(minute='*/1'),
        'args': (1,2),
    },
}