from django.db import models
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from db.models.user import User

import datetime


def get_dir_name(instance, filename):
    return f'houses/house_{instance.pk}/{filename}'


class House(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=75)
    image1 = models.ImageField(upload_to=get_dir_name, blank=True, null=True)
    image2 = models.ImageField(upload_to=get_dir_name, blank=True, null=True)
    image3 = models.ImageField(upload_to=get_dir_name, blank=True, null=True)
    image4 = models.ImageField(upload_to=get_dir_name, blank=True, null=True)
    image5 = models.ImageField(upload_to=get_dir_name, blank=True, null=True)

    @property
    def floors_count(self):
        return self.sections.all().aggregate(models.Count('floors'))['floors__count']

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

    def get_files(self):
        return [self.image1, self.image2, self.image3, self.image4, self.image5]

    def __str__(self):
        return self.name


class HouseUser(models.Model):
    user = models.ForeignKey(User, related_name='houses', on_delete=models.CASCADE)
    house = models.ForeignKey(House, related_name='users', on_delete=models.CASCADE)


class Section(models.Model):
    house = models.ForeignKey(House, related_name='sections', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Floor(models.Model):
    section = models.ForeignKey(Section, related_name='floors', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Measure(models.Model):
    measure_name = models.CharField(max_length=50, unique=True)

    @property
    def service_exists(self):
        if self.services.exists():
            return True
        return False

    def __str__(self):
        return self.measure_name


class Service(models.Model):
    name = models.CharField(max_length=50)
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
    name = models.CharField(max_length=50)
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
    owner = models.ForeignKey(User, related_name='flats', on_delete=models.SET_NULL, blank=True, null=True)
    house = models.ForeignKey(House, related_name='flats', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name='flats', on_delete=models.SET_NULL, blank=True, null=True)
    floor = models.ForeignKey(Floor, related_name='flats', on_delete=models.SET_NULL, blank=True, null=True)
    tariff = models.ForeignKey(Tariff, related_name='flats', on_delete=models.SET_NULL, blank=True, null=True)

    def get_flat_balance(self):
        if not hasattr(self, 'account'):
            return '(нет счета)'
        return self.account.get_account_balance()

    def __str__(self):
        return str(self.number)


class PersonalAccount(models.Model):
    status_choices = [
        (0, 'Активен'),
        (1, 'Неактивен')
    ]

    number = models.IntegerField()
    status = models.IntegerField(choices=status_choices, default=status_choices[0][0])
    house = models.ForeignKey(House, related_name='accounts', on_delete=models.SET_NULL, blank=True, null=True)
    section = models.ForeignKey(Section, related_name='accounts', on_delete=models.SET_NULL, blank=True, null=True)
    floor = models.ForeignKey(Floor, related_name='accounts', on_delete=models.SET_NULL, blank=True, null=True)
    flat = models.OneToOneField(Flat, related_name='account', on_delete=models.SET_NULL, blank=True, null=True)

    def get_account_balance(self):
        if not self.tickets:
            return 0.00
        total_debt = self.tickets.filter(is_done=True, status__in=(1, 2)).aggregate(models.Sum('sum', distinct=True))
        total_paid = 0
        for ticket in self.tickets.all():
            total_paid += ticket.get_ticket_transactions()
        return total_paid - (total_debt['sum__sum'] or 0)

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
    status = models.IntegerField(choices=status_choices, default=2)
    is_done = models.BooleanField(default=0)
    start = models.DateField()
    end = models.DateField()
    section = models.ForeignKey(Section, related_name='tickets', on_delete=models.CASCADE, blank=True, null=True)
    floor = models.ForeignKey(Floor, related_name='tickets', on_delete=models.CASCADE, blank=True, null=True)
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

    def get_ticket_transactions(self):
        return self.transactions.all().aggregate(models.Sum('paid_sum'))['paid_sum__sum'] or 0

    def get_owner(self):
        return self.flat.owner

    @property
    def total_cost(self):
        return self.services.all().aggregate(models.Sum('cost'))['cost__sum'] or 0

    @property
    def ticket_month(self):
        return datetime.date(month=self.created.month, year=self.created.year, day=self.created.day).strftime('%b %Y')

    @property
    def ticket_date(self):
        return datetime.date(month=self.created.month, year=self.created.year, day=self.created.day).strftime('%d.%m.%Y')

    @property
    def has_owner(self):
        if self.flat and self.flat.owner:
            return True
        else:
            return False

    @classmethod
    def total_balance(cls):
        total_debt = cls.objects.filter(is_done=True, status__in=(2, 1)).aggregate(models.Sum('sum', distinct=True))
        total_paid = cls.objects.filter(is_done=True, status__in=(0, 1)).aggregate(models.Sum('transactions__paid_sum'))

        return total_debt['sum__sum'] or 0,\
            (total_paid['transactions__paid_sum__sum'] or 0) - (total_debt['sum__sum'] or 0)

    def __str__(self):
        return f'Квитанция №{self.number}'


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
    floor = models.ForeignKey(Floor, related_name='meters', on_delete=models.CASCADE)
    house = models.ForeignKey(House, related_name='meters', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='meters', on_delete=models.CASCADE)

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

    name = models.CharField(max_length=50, unique=True)
    type = models.IntegerField(choices=type_choices)
    default_income_type = models.BooleanField(default=False)

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
    paid_sum = models.FloatField()
    status = models.BooleanField(default=True)
    manager = models.ForeignKey(User, related_name='master', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    payment_ticket = models.ForeignKey(PaymentTicket, related_name='transactions', on_delete=models.SET_NULL,
                                       blank=True, null=True)

    @property
    def status_display(self):
        if self.status:
            return 'Проведена'
        return 'Непроведена'

    @classmethod
    def get_next_income_number(cls):
        last = cls.objects.filter(payment_item_type__type=0).last()
        if last:
            return last.pk + 1
        else:
            return 1

    @classmethod
    def get_next_outcome_number(cls):
        last = cls.objects.filter(payment_item_type__type=1).last()
        if last:
            return last.pk + 1
        else:
            return 1

    def get_update_url(self):
        if self.payment_item_type.type == 0:
            return reverse('admin_panel:update_income_admin', args=[self.pk])
        else:
            return reverse('admin_panel:update_outcome_admin', args=[self.pk])

    def get_duplicate_url(self):
        if self.payment_item_type.type == 0:
            return reverse('admin_panel:duplicate_income_admin', args=[self.pk])
        else:
            return reverse('admin_panel:duplicate_outcome_admin', args=[self.pk])

    @property
    def transaction_date(self):
        return datetime.date(month=self.created.month, year=self.created.year, day=self.created.day).strftime('%d.%m.%Y')

    @classmethod
    def total_cash(cls):
        income = cls.objects.filter(payment_item_type__type=0,
                                    status=True).aggregate(models.Sum('paid_sum'))['paid_sum__sum'] or 0
        outcome = cls.objects.filter(payment_item_type__type=1,
                                     status=True).aggregate(models.Sum('paid_sum'))['paid_sum__sum'] or 0
        return income - outcome

    def save(self, *args, **kwargs):
        if self.payment_ticket:
            total_paid = (self.payment_ticket.transactions.all()
                          .aggregate(models.Sum('paid_sum'))['paid_sum__sum'] or 0) + self.paid_sum if not self.pk else 0
            if self.payment_ticket.sum <= total_paid:
                self.payment_ticket.status = 0
            elif self.payment_ticket.sum > total_paid:
                self.payment_ticket.status = 1
            self.payment_ticket.save()
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.payment_ticket:
            total_paid = (self.payment_ticket.transactions.all()
                          .aggregate(models.Sum('paid_sum'))['paid_sum__sum'] or 0) - self.paid_sum
            if total_paid == 0:
                self.payment_ticket.status = 2
            elif self.payment_ticket.sum > total_paid:
                self.payment_ticket.status = 1
            self.payment_ticket.save()
        return super().delete(using, keep_parents)


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


class Message(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(blank=True, null=True)
    house = models.ForeignKey(House, related_name='messages', on_delete=models.SET_NULL, blank=True, null=True)
    section = models.ForeignKey(Section, related_name='messages', on_delete=models.SET_NULL, blank=True, null=True)
    floor = models.ForeignKey(Floor, related_name='messages', on_delete=models.SET_NULL, blank=True, null=True)
    flat = models.ForeignKey(Flat, related_name='messages', on_delete=models.SET_NULL, blank=True, null=True)
    with_debt = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.SET_NULL, blank=True, null=True)
    excluded_receivers = models.ManyToManyField(User, related_name='excluded', blank=True)
    owner = models.ForeignKey(User, related_name='owner_messages', on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def message_recipient(self):
        if self.house:
            return True
        else:
            return False

    def __str__(self):
        return self.title


class TicketTemplate(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='file_templates/')
    is_default = models.BooleanField(default=False)

    def get_files(self):
        return [self.file] if self.file else None


class InviteMessage(models.Model):
    phone = models.CharField(max_length=30)
    text = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
