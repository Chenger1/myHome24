from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator

from db.models.manager import UserManager


class Role(models.Model):
    reserved_names = ('Директор', 'Управляющий', 'Бухгалтер', 'Электрик', 'Сантехник')

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

    def __str__(self):
        return self.name


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
    birthday = models.DateField(blank=True, null=True)
    status = models.IntegerField(choices=status_choices, default=status_choices[0][0])

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('phone_number', )

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class User(CustomAbstractUser):
    role = models.ForeignKey(Role, related_name='admin_roles', on_delete=models.CASCADE, blank=True, null=True)
    photo = models.ImageField(upload_to='users/', blank=True, null=True)
    patronym = models.CharField(max_length=100, blank=True, null=True)
    viber = models.CharField(max_length=100, blank=True, null=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    ID = models.IntegerField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    def get_images(self):
        return [self.photo] if self.photo else None

    @classmethod
    def search(cls, data):
        users = cls.objects.all()
        name = data.get('name')
        role = data.get('role')
        phone = data.get('phone')
        email = data.get('email')
        status = data.get('status')
        if name:
            users = users.filter(first_name__in=name, last_name__in=name)
        if role:
            users = users.filter(role=role)
        if phone:
            users = users.filter(phone=phone)
        if email:
            users = users.filter(email=email)
        if status:
            users = users.filter(status=status)
        return users
