from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import JsonResponse
from django.views.generic import View

from rest_api import serializers

from db.models.house import Section, Floor, Flat, TariffService, Meter, PersonalAccount

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
        return queryset


class FloorList(generics.ListAPIView):
    model = Floor
    serializer_class = serializers.FloorSerializer

    def get_queryset(self):
        house = self.request.query_params.get('pk')
        if house:
            queryset = self.model.objects.filter(house__pk=house)
        else:
            queryset = []
        return queryset


class FlatList(generics.ListAPIView):
    model = Flat
    serializer_class = serializers.FlatSerializer

    def get_queryset(self):
        house = self.request.query_params.get('pk')
        if house:
            queryset = self.model.objects.filter(house__pk=house)
        else:
            queryset = []
        return queryset


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
                                    'service': service, 'data': value,
                                    'number': self.model.get_next_meter_number(),
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
            queryset = self.model.objects.all()[20::-1]
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
