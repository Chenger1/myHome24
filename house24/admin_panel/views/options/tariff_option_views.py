from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

from db.models.house import Tariff, Service, TariffService

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
        formset = context['formset']
        if formset.is_valid():
            response = super().form_valid(form)
            if form.is_valid():
                self.object = form.save()
                formset.instance = self.object
                formset.save()
            else:
                return self.form_invalid(form)
            return response
        else:
            return self.form_invalid(form)


class UpdateTariff(UpdateView):
    model = Tariff
    form_class = TariffForm
    formset_class = TariffServiceBlockFormset
    template_name = 'options/tariff/create_tariff.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = self.formset_class(self.request.POST, instance=self.object)
        else:
            context['formset'] = self.formset_class(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            response = super().form_valid(form)
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


class DeleteTariff(View):
    model = Tariff
    success_url = 'admin_panel:list_tariff_admin'

    def get(self, request, pk):
        tariff = get_object_or_404(Tariff, pk=pk)
        if tariff:
            tariff.delete()
        return redirect(self.success_url)


class DeleteTariffService(View):
    model = TariffService

    def get(self, request):
        service = get_object_or_404(TariffService, pk=request.GET.get('pk'))
        service.delete()
        return JsonResponse({'status': 200})
