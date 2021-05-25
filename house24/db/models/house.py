from django.db import models
from django.urls import reverse

from db.models.user import User


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

    def __str__(self):
        return self.measure_name


class Service(models.Model):
    name = models.CharField(max_length=100)
    measure = models.ForeignKey(Measure, related_name='services', on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=1)

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
    price = models.IntegerField()
    currency = models.CharField(max_length=30, default='грн.')


class PersonalAccount(models.Model):
    number = models.IntegerField()
    status = models.BooleanField(default=0)
    house = models.ForeignKey(House, related_name='accounts', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name='accounts', on_delete=models.CASCADE)


class Flat(models.Model):
    number = models.IntegerField()
    square = models.IntegerField()
    owner = models.ForeignKey(User, related_name='flats', on_delete=models.CASCADE)
    house = models.ForeignKey(House, related_name='flats', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name='flats', on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, related_name='flats', on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, related_name='flats', on_delete=models.CASCADE)
    personal_account = models.ForeignKey(PersonalAccount, related_name='flats', on_delete=models.CASCADE)


class PaymentTicket(models.Model):
    status_choices = [
        (0, 'Оплачена'),
        (1, 'Частично оплачена'),
        (2, 'Неоплачена')
    ]

    number = models.IntegerField()
    status = models.IntegerField(choices=status_choices, default=status_choices[2])
    is_done = models.BooleanField(default=0)
    start = models.DateField()
    end = models.DateField()
    section = models.ForeignKey(Section, related_name='tickets', on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, related_name='tickets', on_delete=models.CASCADE)
    personal_account = models.ForeignKey(PersonalAccount, related_name='tickets', on_delete=models.CASCADE)
    house = models.ForeignKey(House, related_name='tickets', on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, related_name='tickets', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='tickets', on_delete=models.CASCADE)
    created = models.DateField()


class Meter(models.Model):
    number = models.IntegerField()
    date = models.DateField()
    status = models.BooleanField()
    data = models.DateField()
    flat = models.ForeignKey(Flat, related_name='meters', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name='meters', on_delete=models.CASCADE)
    house = models.ForeignKey(House, related_name='meters', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='meters', on_delete=models.CASCADE)


class PaymentItem(models.Model):
    type_choices = [
        (0, 'Приход'),
        (1, 'Расход')
    ]

    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=type_choices)


class Income(models.Model):
    number = models.IntegerField()
    created = models.DateField()
    owner = models.ForeignKey(User, related_name='owner_incomes', on_delete=models.CASCADE)
    personal_account = models.ForeignKey(PersonalAccount, related_name='incomes', on_delete=models.CASCADE)
    type = models.ForeignKey(PaymentItem, related_name='incomes', on_delete=models.CASCADE)
    sum = models.IntegerField()
    status = models.BooleanField(default=0)
    manager = models.ForeignKey(User, related_name='master_incomes', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()


class Outcome(models.Model):
    number = models.IntegerField()
    created = models.DateField()
    type = models.ForeignKey(PaymentItem, related_name='outcomes', on_delete=models.CASCADE)
    sum = models.IntegerField()
    status = models.BooleanField(default=0)
    manager = models.ForeignKey(User, related_name='outcomes', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()


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
    comment = models.TextField()
    type = models.IntegerField(choices=type_choices, default=type_choices[0])
    status = models.IntegerField(choices=status_choices)
    owner = models.ForeignKey(User, related_name='owner_requests', on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, related_name='requests', on_delete=models.CASCADE)
    master = models.ForeignKey(User, related_name='master_requests', on_delete=models.CASCADE)
