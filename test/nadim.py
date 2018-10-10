# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Exe file to Run"
"""

from celery import Celery

app = Celery('nadim', broker="amqp://localhost//", backend="mongodb://aldrin:starwars0@ds259802.mlab.com:59802/aldrin")

@app.task
def something(_s):
    return _s