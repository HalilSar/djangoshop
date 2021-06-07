from celery import shared_task
from time import sleep
from django.core.mail import send_mail
@shared_task
def sleepy(duration):
    sleep(duration)
    return None

@shared_task
def send_email_task(email):
    # sleep(10)
    email.send(fail_silently=False)
    return None