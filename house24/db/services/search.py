from django.db.models import Value
from django.db.models.functions import Concat

from db.models.house import House, Flat, PersonalAccount, PaymentTicket, Message, Meter, Transaction, MasterRequest
from db.models.user import User


class HouseSearch:
    @staticmethod
    def search(form_data, queryset):
        return queryset.filter(name__icontains=form_data.get('name'), address__icontains=form_data.get('address'))


class FlatSearch:
    @staticmethod
    def search(form_data, queryset):
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
    def search(form_data, queryset):
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
    def search(form_data, queryset):
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
    def search(form_data, queryset):
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
    def search(form_data, queryset):
        queryset = queryset.filter(number__icontains=form_data.get('number'))
        if form_data.get('status'):
            queryset = queryset.filter(status=form_data.get('status'))
        if form_data.get('start') or form_data.get('end'):
            queryset = queryset.filter(start__range=[form_data.get('start'), form_data.get('end')],
                                       end__range=[form_data.get('start'), form_data.get('end')])
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
    def search(form_data, queryset):
        return queryset.filter(title__icontains=form_data.get('text'))


class MeterSearch:
    @staticmethod
    def search(form_data, queryset):
        if form_data.get('house'):
            queryset = queryset.filter(house=form_data.get('house'))
        if form_data.get('section'):
            queryset = queryset.filter(section=form_data.get('section'))
        if form_data.get('flat'):
            queryset = queryset.filter(flat__number__icontains=form_data.get('flat'))
        if form_data.get('service'):
            queryset = queryset.filter(service=form_data.get('service'))
        return queryset


class MeterHistorySearch:
    @staticmethod
    def search(form_data):
        queryset = Meter.objects.filter(flat__pk=form_data['flat'])
        queryset = queryset.filter(number__contains=form_data.get('number'))
        if form_data.get('status'):
            queryset = queryset.filter(status=form_data.get('status'))
        if form_data.get('start') or form_data.get('end'):
            queryset = queryset.filter(date__range=[form_data.get('start'), form_data.get('end')])
        if form_data.get('house'):
            queryset = queryset.filter(house=form_data.get('house'))
        if form_data.get('section'):
            queryset = queryset.filter(section=form_data.get('section'))
        if form_data.get('service'):
            queryset = queryset.filter(service=form_data.get('service'))
        return queryset


class TransactionSearch:
    @staticmethod
    def search(form_data, queryset):
        if form_data.get('number'):
            queryset = queryset.filter(number__contains=form_data.get('number'))
        if form_data.get('start') or form_data.get('end'):
            queryset = queryset.filter(created__range=[form_data.get('start'), form_data.get('end')])
        if form_data.get('status'):
            queryset = queryset.filter(status=form_data.get('status'))
        if form_data.get('payment_item_type'):
            queryset = queryset.filter(payment_item_type=form_data.get('payment_item_type'))
        if form_data.get('owner'):
            queryset = queryset.filter(owner=form_data.get('owner'))
        if form_data.get('personal_account'):
            queryset = queryset.filter(personal_account__contains=form_data.get('personal_account'))
        if form_data.get('income_outcome'):
            queryset = queryset.filter(payment_item_type__type=form_data.get('income_outcome'))
        return queryset


class MasterRequestSearch:
    @staticmethod
    def search(form_data, queryset):
        if form_data.get('number'):
            queryset = queryset.filter(pk__contains=form_data.get('number'))
        if form_data.get('start') or form_data.get('end'):
            queryset = queryset.filter(date__range=[form_data.get('start'), form_data.get('end')])
        if form_data.get('master_type'):
            queryset = queryset.filter(type=form_data.get('master_type'))
        if form_data.get('description'):
            queryset = queryset.filter(comment__icontains=form_data.get('description'))
        if form_data.get('flat'):
            queryset = queryset.filter(flat__number__contains=form_data.get('flat'))
        if form_data.get('owner'):
            queryset = queryset.filter(owner=form_data.get('owner'))
        if form_data.get('phone'):
            queryset = queryset.filter(owner__phone_number__contains=form_data.get('phone'))
        if form_data.get('master'):
            queryset = queryset.filter(master=form_data.get('master'))
        if form_data.get('status'):
            queryset = queryset.filter(status=form_data.get('status'))
        return queryset
