from config.celery import app
from django.core.mail import EmailMessage


@app.task
def send_email(data):
    email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    email.send()