from django.core.management import BaseCommand

from training.models import Course, Lesson, Payment
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Payment.objects.all().delete()

        payments_list = [
            {'user': User.objects.get(pk=1), 'payment_date': '2023-01-01 12:00:00', 'course': Course.objects.get(pk=1),
             'amount': "1111", 'payment_method': 'BANK_TRANSFER'},
            {'user': User.objects.get(pk=2), 'payment_date': '2023-02-02 11:00:00', 'course': Course.objects.get(pk=1),
             'amount': "2222", 'payment_method': 'CASH'},
            {'user': User.objects.get(pk=3), 'payment_date': '2023-03-03 10:00:00', 'lesson': Lesson.objects.get(pk=1),
             'amount': "3333", 'payment_method': 'CASH'},
            {'user': User.objects.get(pk=4), 'payment_date': '2023-04-04 09:00:00', 'lesson': Lesson.objects.get(pk=2),
             'amount': "4444", 'payment_method': 'BANK_TRANSFER'}
        ]

        payments = []
        for payment in payments_list:
            payments.append(Payment(**payment))
        Payment.objects.bulk_create(payments)
