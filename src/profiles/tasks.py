from __future__ import absolute_import, unicode_literals
from config.celery import app
from .service import send


@app.task
def send_email_task(data):
    send(data)