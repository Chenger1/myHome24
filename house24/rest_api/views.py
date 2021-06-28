from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.db.models import Sum

from rest_api import serializers

from db.models.house import Section, Floor, Flat, TariffService, Meter, PersonalAccount, PaymentTicket, Transaction
from db.services.utils import generate_next_instance_number

from admin_panel.forms.meters_forms import CreateMeterForm

import json


class SectionList(generics.ListAPIView):
    model = Section
    serializer_class = serializers.SectionSerializer

    def get_queryset(self):
        house = self.request.query_params.get('pk')
        if house:
            queryset = self.model.objects.filter(house__pk=house)
        else:
            queryset = []
        return queryset.order_by('-name')


class FloorList(generics.ListAPIView):
    model = Floor
    serializer_class = serializers.FloorSerializer

    def get_queryset(self):
        section = self.request.query_params.get('pk')
        if section:
            queryset = self.model.objects.filter(section__pk=section)
        else:
            queryset = []
        return queryset.order_by('-name')


class FlatList(generics.ListAPIView):
    model = Flat
    serializer_class = serializers.FlatSerializer

    def get_queryset(self):
        flat = self.request.query_params.get('pk')
        if flat:
            queryset = self.model.objects.filter(floor__pk=flat)
        else:
            queryset = []
        return queryset.order_by('-number')


class GetTariffServices(View):
    model = TariffService

    def get(self, request):
        services = self.model.objects.filter(tariff__pk=request.GET.get('pk'))
        return JsonResponse(self.serialize(services))

    def serialize(self, queryset):
        result = {}
        for index, inst in enumerate(queryset):
            result.update({index: {
                'id': inst.service.pk,
                'name': inst.service.name,
                'price': inst.price,
                'measure': inst.service.measure.measure_name
            }})
        return result


class CreateMeterApiView(View):
    model = Meter
    form = CreateMeterForm

    def get(self, request):
        data = json.loads(request.GET.get('data'))
        for service, value in data['data'].items():
            form = CreateMeterForm({'date': data['date'], 'house': data['house'],
                                   'section': data['section'], 'flat': data['flat'],
                                    'floor': data['floor'],
                                    'service': service, 'data': value,
                                    'number': generate_next_instance_number(self.model),
                                    'status': 0})
            if form.is_valid():
                form.save()
            else:
                return JsonResponse({'status': 400})
        return JsonResponse({'status': 200})


class GetMeterDataApiView(View):
    model = Meter

    def get(self, request):
        flat_pk = request.GET.get('pk')
        if flat_pk:
            queryset = self.model.objects.filter(flat__pk=flat_pk).order_by('-id')[:20]
        else:
            queryset = self.model.objects.all().order_by('-id')[:20]
        serialized = self.serialize(queryset)
        return JsonResponse(serialized)

    def serialize(self, queryset):
        result = {}
        for index, inst in enumerate(queryset):
            result.update({index: {
                'number': inst.number,
                'status': inst.status,
                'date': inst.meter_date,
                'month': inst.meter_month,
                'house': inst.house.name,
                'section': inst.section.name,
                'flat': inst.flat.number,
                'service': inst.service.name,
                'data': inst.data,
                'measure': inst.service.measure.measure_name
            }})
        return result


class OwnerFlatList(APIView):
    model = Flat

    def get(self, request):
        owner = request.GET.get('pk')
        if owner:
            queryset = self.model.objects.filter(owner__pk=owner)
        else:
            queryset = self.model.objects.all()
        return Response(self.serialize(queryset))

    def serialize(self, queryset):
        """
        Serialize queryset in select2 widget format
        :param queryset:
        :return:
        """
        result = {'results': []}
        for item in queryset:
            result['results'].append({
                'id': item.pk,
                'text': f'{item.number}, {item.house.name}'
            })
        return result


class OwnerPersonalAccounts(APIView):
    model = PersonalAccount

    def get(self, request):
        owner = request.GET.get('pk')
        if owner:
            queryset = self.model.objects.filter(flat__owner__pk=owner)
        else:
            queryset = self.model.objects.all()
        return Response(self.serialize(queryset))

    def serialize(self, queryset):
        """
        Serialize queryset in select2 widget format
        :param queryset:
        :return:
        """
        result = {'results': []}
        for item in queryset:
            result['results'].append({
                'id': item.pk,
                'text': item.number
            })
        return result


class PersonalAccountPaymentTicketList(APIView):
    model = PaymentTicket

    def get(self, request):
        account = request.GET.get('pk')
        if account:
            queryset = self.model.objects.filter(personal_account__pk=account,
                                                 status__in=[1, 2])
        else:
            queryset = self.model.objects.filter(status__in=[1, 2])
        return Response(self.serialize(queryset))

    def serialize(self, queryset):
        """
        Serialize queryset in select2 widget format
        :param queryset:
        :return:
        """
        result = {'results': []}
        for item in queryset:
            result['results'].append({
                'id': item.pk,
                'text': item.__str__()
            })
        return result


class TotalBalance(APIView):
    model = Transaction

    def get(self, request):
        return Response({'total_cash': self.model.total_cash()})


class PersonalAccountStatus(APIView):
    model = PersonalAccount

    def get(self, request):
        account = get_object_or_404(self.model, pk=self.request.GET.get('pk'))
        if account.status == 0 and account.flat:
            return Response({'status': True})
        else:
            return Response({'status': False})


class PaymentTicketSum(APIView):
    model = PaymentTicket

    def get(self, request):
        ticket = get_object_or_404(self.model, pk=request.GET.get('pk'))
        total_paid = ticket.transactions.all().aggregate(Sum('paid_sum'))['paid_sum__sum'] or 0
        return Response({'sum': (ticket.sum - total_paid)})


class FlatPersonalAccount(APIView):
    model = PersonalAccount

    def get(self, request):
        if request.GET.get('pk'):
            queryset = PersonalAccount.objects.filter(flat__pk=request.GET.get('pk'))
        else:
            queryset = PersonalAccount.objects.all()
        return Response(self.serialize(queryset))

    def serialize(self, queryset):
        """
        Serialize queryset in select2 widget format
        :param queryset:
        :return:
        """
        result = {'results': []}
        for item in queryset:
            result['results'].append({
                'id': item.pk,
                'text': item.number
            })
        return result
