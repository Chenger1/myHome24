from django.db.models import Value
from django.db.models.functions import Concat

from db.models.house import House, Flat, PersonalAccount, PaymentTicket, Message
from db.models.user import User


class HouseSearch:
    @staticmethod
    def search(form_data):
        return House.objects.filter(name__icontains=form_data.get('name'), address__icontains=form_data.get('address'))


class FlatSearch:
    @staticmethod
    def search(form_data):
        queryset = Flat.objects.all()
        if form_data.get('number'):
            queryset = queryset.filter(number__icontains=form_data.get('number'))
        if form_data.get('house'):
            queryset = queryset.filter(house=form_data.get('house'))
        if form_data.get('section'):
            queryset = queryset.filter(section=form_data.get('section'))
        if form_data.get('floor'):
            queryset = queryset.filter(floor=form_data.get('floor'))
        if form_data.get('user'):
            queryset = queryset.filter(owner=form_data.get('user'))
        if form_data.get('debt'):
            queryset = queryset.filter(owner__isnull=False)
            queryset = [instance for instance in queryset if instance.owner.has_debt == bool(int(form_data.get('debt')))]
        return queryset


class OwnerSearch:
    @staticmethod
    def search(form_data):
        queryset = User.objects.filter(is_staff=False)
        queryset = queryset.annotate(fullname=Concat('first_name', Value(' '), 'last_name'))
        queryset = queryset.filter(fullname__icontains=form_data.get('username'),
                                   email__contains=form_data.get('email'),
                                   phone_number__contains=form_data.get('phone'))
        if form_data.get('id_field'):
            queryset = queryset.filter(pk=form_data.get('id_field'))
        if form_data.get('house'):
            queryset = queryset.filter(flats__house=form_data.get('house')).distinct()
        if form_data.get('flat'):
            queryset = queryset.filter(flats__number__icontains=form_data.get('flat')).distinct()
        if form_data.get('date_joined'):
            queryset = queryset.filter(date_joined=form_data.get('date_joined'))
        if form_data.get('status'):
            queryset = queryset.filter(status=form_data.get('status'))
        if form_data.get('is_debt'):
            queryset = [instance for instance in queryset if instance.has_debt == bool(int(form_data.get('is_debt')))]
        return queryset


class UserSearch:
    @staticmethod
    def search(form_data):
        queryset = User.objects.filter(is_staff=True)
        queryset = queryset.annotate(fullname=Concat('first_name', Value(' '), 'last_name'))
        queryset = queryset.filter(fullname__icontains=form_data.get('username'),
                                   email__contains=form_data.get('email'),
                                   phone_number__contains=form_data.get('phone'))
        if form_data.get('role'):
            queryset = queryset.filter(role=form_data.get('role'))
        if form_data.get('status'):
            queryset = queryset.filter(status=form_data.get('status'))
        return queryset


class PersonalAccountSearch:
    @staticmethod
    def search(form_data):
        queryset = PersonalAccount.objects.all()
        queryset = queryset.filter(number__icontains=form_data.get('number'))
        if form_data.get('status'):
            queryset = queryset.filter(status=form_data.get('status'))
        if form_data.get('flat'):
            queryset = queryset.filter(flat__number__icontains=form_data.get('flat'))
        if form_data.get('house'):
            queryset = queryset.filter(house=form_data.get('house'))
        if form_data.get('section'):
            queryset = queryset.filter(section=form_data.get('section'))
        if form_data.get('user'):
            queryset = queryset.filter(flat__owner=form_data.get('user'))
        if form_data.get('debt'):
            queryset = queryset.filter(flat__owner__isnull=False)
            queryset = [instance for instance in queryset if instance.has_debt == bool(int(form_data.get('is_debt')))]
        return queryset


class PaymentTicketSearch:
    @staticmethod
    def search(form_data):
        queryset = PaymentTicket.objects.all()
        queryset = queryset.filter(number__icontains=form_data.get('number'))
        if form_data.get('status'):
            queryset = queryset.filter(status=form_data.get('status'))
        if form_data.get('start'):
            queryset = queryset.filter(start=form_data.get('start'))
        if form_data.get('end'):
            queryset = queryset.filter(end=form_data.get('end'))
        if form_data.get('month'):
            month = int(form_data.get('month').split('-')[-1])
            queryset = queryset.filter(created__month=month)
        if form_data.get('flat'):
            queryset = queryset.filter(flat__number__icontains=form_data.get('flat'))
        if form_data.get('owner'):
            queryset = queryset.filter(flat__owner=form_data.get('owner'))
        if form_data.get('is_done'):
            queryset = queryset.filter(is_done=bool(int(form_data.get('is_done'))))
        return queryset


class MessageSearch:
    @staticmethod
    def search(form_data):
        return Message.objects.filter(title__icontains=form_data.get('text'))
