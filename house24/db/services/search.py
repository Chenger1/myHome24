from django.db.models import Value
from django.db.models.functions import Concat

from db.models.house import House, Flat


class HouseSearch:
    @staticmethod
    def search(form_data):
        return House.objects.filter(name__icontains=form_data.get('name'), address__icontains=form_data.get('address'))


# class FlatSearch:
#     @staticmethod
#     def search(form_data):
#         # queryset = Flat.objects.annotate(fullname=Concat('owner__first_name', Value(' '), 'owner__last_name'))
#         # return queryset.filter(pk__contains=form_data.get('number'),
#         #                        )
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
            queryset = [instance for instance in queryset if instance.owner.has_debt
                        and instance.owner.has_debt == bool(int(form_data.get('debt')))]
        return queryset
