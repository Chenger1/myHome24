from django.db import models
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from db.models.user import User

import datetime


class House(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    image1 = models.ImageField()
    image2 = models.ImageField()
    image3 = models.ImageField()
    image4 = models.ImageField()
    image5 = models.ImageField()

    @classmethod
    def search(cls, data):
        houses = cls.objects.all()
        name = data.get('name')
        address = data.get('address')
        if name:
            houses = houses.filter(name__contains=name)
        if address:
            houses = houses.filter(address__contains=address)
        return houses

    def __str__(self):
        return self.name


class HouseUser(models.Model):
    user = models.ForeignKey(User, related_name='houses', on_delete=models.CASCADE)
    house = models.ForeignKey(House, related_name='users', on_delete=models.CASCADE)


class Section(models.Model):
    house = models.ForeignKey(House, related_name='sections', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Floor(models.Model):
    house = models.ForeignKey(House, related_name='floors', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Measure(models.Model):
    measure_name = models.CharField(max_length=50)

    @property
    def service_exists(self):
        if self.services.exists():
            return True
        return False

    def __str__(self):
        return self.measure_name


class Service(models.Model):
    name = models.CharField(max_length=100)
    measure = models.ForeignKey(Measure, related_name='services', on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=1)

    @property
    def tariff_exists(self):
        if self.tariffs.exists():
            return True
        return False

    def __str__(self):
        return self.name


class Tariff(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    updated = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return reverse('admin_panel:update_tariff', args=[self.pk])

    def __str__(self):
        return self.name


class TariffService(models.Model):
    tariff = models.ForeignKey(Tariff, related_name='services', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='tariffs', on_delete=models.CASCADE)
    price = models.FloatField()
    currency = models.CharField(max_length=30, default='грн.')


class Flat(models.Model):
    number = models.IntegerField()
    square = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey(User, related_name='flats', on_delete=models.CASCADE, blank=True, null=True)
    house = models.ForeignKey(House, related_name='flats', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name='flats', on_delete=models.CASCADE, blank=True, null=True)
    floor = models.ForeignKey(Floor, related_name='flats', on_delete=models.CASCADE, blank=True, null=True)
    tariff = models.ForeignKey(Tariff, related_name='flats', on_delete=models.CASCADE, blank=True, null=True)

    @classmethod
    def search(cls, data):
        return cls.objects.all()

    def __str__(self):
        return str(self.number)


class PersonalAccount(models.Model):
    status_choices = [
        (0, 'Активен'),
        (1, 'Неактивен')
    ]

    number = models.IntegerField()
    status = models.IntegerField(choices=status_choices, default=status_choices[0][0])
    house = models.ForeignKey(House, related_name='accounts', on_delete=models.CASCADE, blank=True, null=True)
    section = models.ForeignKey(Section, related_name='accounts', on_delete=models.CASCADE, blank=True, null=True)
    flat = models.OneToOneField(Flat, related_name='account', on_delete=models.SET_NULL, blank=True, null=True)

    @classmethod
    def get_next_account_number(cls):
        last = cls.objects.last()
        if last:
            return last.pk + 1
        else:
            return 1

    @classmethod
    def find_inst(cls, number):
        try:
            return cls.objects.get(number=number)
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return str(self.number)


class PaymentTicket(models.Model):
    status_choices = [
        (0, 'Оплачена'),
        (1, 'Частично оплачена'),
        (2, 'Неоплачена')
    ]

    number = models.IntegerField()
    status = models.IntegerField(choices=status_choices, default=status_choices[0][1])
    is_done = models.BooleanField(default=0)
    start = models.DateField()
    end = models.DateField()
    section = models.ForeignKey(Section, related_name='tickets', on_delete=models.CASCADE, blank=True, null=True)
    flat = models.ForeignKey(Flat, related_name='tickets', on_delete=models.CASCADE)
    personal_account = models.ForeignKey(PersonalAccount, related_name='tickets', on_delete=models.CASCADE,
                                         blank=True, null=True)
    house = models.ForeignKey(House, related_name='tickets', on_delete=models.CASCADE, blank=True, null=True)
    tariff = models.ForeignKey(Tariff, related_name='tickets', on_delete=models.CASCADE, blank=True, null=True)
    sum = models.FloatField()
    created = models.DateField()

    @classmethod
    def get_next_ticket_number(cls):
        last = cls.objects.last()
        if last:
            return last.pk + 1
        else:
            return 1

    @property
    def ticket_month(self):
        return datetime.date(month=self.created.month, year=self.created.year, day=self.created.day).strftime('%b %Y')

    @property
    def ticket_date(self):
        return datetime.date(month=self.created.month, year=self.created.year, day=self.created.day).strftime('%d.%m.%Y')


class PaymentTicketService(models.Model):
    payment_ticket = models.ForeignKey(PaymentTicket, related_name='services', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='payment_tickets_service', on_delete=models.CASCADE)
    outcome = models.FloatField()
    unit_price = models.FloatField()
    cost = models.FloatField()


class Meter(models.Model):
    status_choices = [
        (0, 'Новое'),
        (1, 'Учтено'),
        (2, 'Учтено и оплачен'),
        (3, 'Нулевое')
    ]

    number = models.IntegerField()
    date = models.DateField()
    status = models.IntegerField(choices=status_choices, default=status_choices[0][0])
    data = models.IntegerField()
    flat = models.ForeignKey(Flat, related_name='meters', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name='meters', on_delete=models.CASCADE)
    house = models.ForeignKey(House, related_name='meters', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='meters', on_delete=models.CASCADE)

    @classmethod
    def get_next_meter_number(cls):
        last = cls.objects.last()
        if last:
            return last.pk + 1
        else:
            return 1

    @property
    def meter_month(self):
        return datetime.date(month=self.date.month, year=self.date.year, day=self.date.day).strftime('%b %Y')

    @property
    def meter_date(self):
        return datetime.date(month=self.date.month, year=self.date.year, day=self.date.day).strftime('%d.%m.%Y')


class PaymentItem(models.Model):
    type_choices = [
        (0, 'Приход'),
        (1, 'Расход')
    ]

    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=type_choices)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    number = models.IntegerField()
    created = models.DateField()
    owner = models.ForeignKey(User, related_name='owner_transfer', on_delete=models.CASCADE, blank=True, null=True)
    personal_account = models.ForeignKey(PersonalAccount, related_name='transfers', on_delete=models.CASCADE,
                                         blank=True, null=True)
    payment_item_type = models.ForeignKey(PaymentItem, related_name='transfers', on_delete=models.CASCADE,
                                          blank=True, null=True)
    amount = models.IntegerField()
    status = models.BooleanField(default=True)
    manager = models.ForeignKey(User, related_name='master', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()

    @classmethod
    def get_next_transaction_number(cls):
        last = cls.objects.last()
        if last:
            return last.pk + 1
        else:
            return 1

    @property
    def transaction_date(self):
        return datetime.date(month=self.created.month, year=self.created.year, day=self.created.day).strftime('%d.%m.%Y')


class MasterRequest(models.Model):
    type_choices = [
        (0, 'Любой специалист'),
        (1, 'Сантехник'),
        (2, 'Электрик'),
        (3, 'Слесарь')
    ]
    status_choices = [
        (0, 'Новое'),
        (1, 'В работе'),
        (2, 'Выполнено')
    ]

    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    comment = models.TextField(blank=True, null=True)
    type = models.IntegerField(choices=type_choices, default=type_choices[0][0])
    status = models.IntegerField(choices=status_choices, default=[0][0])
    owner = models.ForeignKey(User, related_name='owner_requests', on_delete=models.CASCADE,
                              blank=True, null=True)
    flat = models.ForeignKey(Flat, related_name='requests', on_delete=models.CASCADE)
    master = models.ForeignKey(User, related_name='master_requests', on_delete=models.CASCADE,
                               blank=True, null=True)
