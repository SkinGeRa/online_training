from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def user_disconnection():
    expiry_date = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(last_login__lte=expiry_date)
    inactive_users.update(is_active=False)