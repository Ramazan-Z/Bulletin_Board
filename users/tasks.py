import sys

from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@shared_task
def send_email_info(subject, message, recipient_list):
    """Фоновая отправка уведомлений пользователю."""
    from_email = EMAIL_HOST_USER
    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
