from django.db import models
from django.utils import timezone

from config import settings
from users.models import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    preview = models.ImageField(upload_to='training/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты', default=50)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              verbose_name='Пользователь', **NULLABLE)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='training/', verbose_name='Превью', **NULLABLE)
    video_url = models.URLField(max_length=250, verbose_name='Ссылка на видео', **NULLABLE)

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты', default=50)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='Подписка')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    sub_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.course} {self.user} ({self.is_active})'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
