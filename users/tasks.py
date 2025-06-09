from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def off_users_active():
    now = timezone.now()
    users = User.objects.filter(last_login__lt=now - timedelta(days=30), is_active=True, is_superuser=False)
    if users.exists():
        users.update(is_active=False)

