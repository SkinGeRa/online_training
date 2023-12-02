from django.db import models

from config import settings
from training.models import Lesson, Course
from users.models import NULLABLE


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('CASH', 'Наличные'),
        ('BANK_TRANSFER', 'Перевод на счет'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateTimeField(verbose_name='Дата оплаты', **NULLABLE)

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)

    amount = models.PositiveSmallIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Cпособ оплаты',
                                      default='BANK_TRANSFER')
    stripe_id = models.CharField(max_length=300, verbose_name='stripe_id', **NULLABLE)

    def __str__(self):
        return f'{self.user} {self.amount} {self.payment_method}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

