from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_async(to_email, subject, message, from_email):
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[to_email],
        from_email=from_email,
    )
