from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator

from db.models.manager import UserManager


class Role(models.Model):
    name = models.CharField(max_length=100)
    statistic = models.BooleanField(default=1)
    cashbox = models.BooleanField(default=1)
    ticket = models.BooleanField(default=1)
    personal_account = models.BooleanField(default=1)
    flats = models.BooleanField(default=1)
    owners = models.BooleanField(default=1)
    houses = models.BooleanField(default=1)
    messages = models.BooleanField(default=1)
    master_request = models.BooleanField(default=1)
    meters = models.BooleanField(default=1)
    site_control = models.BooleanField(default=1)
    services = models.BooleanField(default=1)
    tariffs = models.BooleanField(default=1)
    roles = models.BooleanField(default=1)
    users = models.BooleanField(default=1)
    credentials = models.BooleanField(default=1)


class CustomAbstractUser(AbstractBaseUser, PermissionsMixin):
    status_choices = [
        (0, 'Активен'),
        (1, 'Новый'),
        (2, 'Отключен')
    ]

    phone_validation = RegexValidator(regex=r'^\+\d{8,15}$', message='Неправильный формат номера.')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, validators=[phone_validation])
    birthday = models.DateField()
    status = models.IntegerField(choices=status_choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['__all__']

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()


class User(CustomAbstractUser):
    role = models.ForeignKey(Role, related_name='admin_users', on_delete=models.CASCADE)


class Owner(CustomAbstractUser):
    photo = models.ImageField()
    patronym = models.CharField(max_length=100)
    viber = models.CharField(max_length=100, blank=True, null=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    ID = models.IntegerField()
    about = models.TextField()
