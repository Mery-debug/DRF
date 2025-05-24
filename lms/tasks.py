from celery import shared_task
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail


@shared_task
def send_email(course_name, email):
    send_mail('Обновление курса',
              f'Вышло обновление в курсе {course_name}',
              EMAIL_HOST_USER,
              [email]
              )

