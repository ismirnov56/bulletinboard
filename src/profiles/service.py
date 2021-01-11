from django.core.mail import send_mail


def send(data):
    """
    Функция для отправки email
    """
    send_mail(
        subject=data['email_subject'],
        message=data['email_body'],
        from_email='noreplay@bulletinboard.com',
        recipient_list=[data['to_email']],
        fail_silently=False
    )
