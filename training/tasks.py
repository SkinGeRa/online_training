from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_update_course(course_name, user_emails):
    subject = 'Курс обновился!'
    message = f'Материалы курса "{course_name}" обновились!'
    from_email = None
    recipient_list = user_emails

    send_mail(subject, message, from_email, recipient_list)