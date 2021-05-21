from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from db.models.house import Tariff, Service

from admin_panel.forms.system_options_forms import TariffForm, TariffServiceBlockFormset


class ListTariff(ListView):
    model = Tariff
    template_name = 'options/tariff/tariff_list.html'
    context_object_name = 'tariffs'


class CreateTariff(CreateView):
    model = Tariff
    form_class = TariffForm
    formset_class = TariffServiceBlockFormset
    template_name = 'options/tariff/create_tariff.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = self.formset_class(self.request.POST)
        else:
            context['formset'] = self.formset_class()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        response = super().form_valid(form)
        formset = context['formset']
        if formset.is_valid():
            formset.save()
            return response
        else:
            return self.form_invalid(form)


class GetServiceMeasure(View):
    model = Service

    def get(self, request):
        service = get_object_or_404(Service, pk=request.GET.get('pk'))
        measure = service.measure.measure_name
        return JsonResponse({'measure_name': measure})
