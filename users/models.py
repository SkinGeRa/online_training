from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'null': True, 'blank': True}


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=50, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)

    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'