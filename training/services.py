from django.core.mail import send_mail
from django.conf import settings


def send_sub_message(email, course):
    send_mail(
        'Подписка',
        f'У вас оформлена подписка на {course}',
        settings.EMAIL_HOST_USER,
        [email]
    )
