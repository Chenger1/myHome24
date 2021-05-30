from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.urls import reverse_lazy

from db.models.house import Tariff, Service, TariffService

from admin_panel.forms.system_options_forms import TariffForm, TariffServiceBlockFormset
from admin_panel.views.mixins import DeleteInstanceView, DeleteInstanceWithoutReload
from admin_panel.permission_mixin import AdminPermissionMixin


class ListTariff(AdminPermissionMixin, ListView):
    model = Tariff
    template_name = 'options/tariff/tariff_list.html'
    context_object_name = 'tariffs'

    def get_queryset(self):
        return self.model.objects.all()[::-1]


class CreateTariff(AdminPermissionMixin, CreateView):
    model = Tariff
    form_class = TariffForm
    formset_class = TariffServiceBlockFormset
    template_name = 'options/tariff/create_tariff.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin_panel:list_tariff_admin')

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


class UpdateTariff(AdminPermissionMixin, UpdateView):
    model = Tariff
    form_class = TariffForm
    formset_class = TariffServiceBlockFormset
    template_name = 'options/tariff/create_tariff.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin_panel:list_tariff_admin')

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


class GetServiceMeasure(AdminPermissionMixin, View):
    model = Service

    def get(self, request):
        service = get_object_or_404(Service, pk=request.GET.get('pk'))
        measure = service.measure.measure_name
        return JsonResponse({'measure_name': measure})


class DeleteTariff(DeleteInstanceView):
    model = Tariff
    redirect_url = 'admin_panel:list_tariff_admin'


class DeleteTariffService(DeleteInstanceWithoutReload):
    model = TariffService


class DuplicateTariff(AdminPermissionMixin, View):
    model = Tariff
    form_class = TariffForm
    formset_class = TariffServiceBlockFormset
    template_name = 'options/tariff/create_tariff.html'
    context_object_name = 'form'

    def get(self, request, pk):
        base_inst = get_object_or_404(Tariff, pk=pk)
        form = self.form_class(instance=base_inst)
        formset = self.formset_class(instance=base_inst)
        return render(request, self.template_name, context={self.context_object_name: form,
                                                            'formset': formset})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            old_obj = get_object_or_404(Tariff, pk=pk)
            form.instance.pk = None
            obj = form.save()
            formset = self.formset_class(request.POST, instance=old_obj)
            if formset.is_valid():
                for form in formset:
                    if not form.empty_permitted and form.has_changed():
                        #  If form is empty - just pass
                        form.instance.pk = None
                        new_form = form.save(commit=False)
                        new_form.tariff = obj
                        new_form.save()
                return redirect('admin_panel:list_tariff_admin')
            else:
                obj.delete()
                return render(request, self.template_name, context={self.context_object_name: form,
                                                                    'formset': formset})
        return render(request, self.template_name, context={self.context_object_name: form})


class DetailTariffView(AdminPermissionMixin, DetailView):
    model = Tariff
    template_name = 'options/tariff/detail_tariff.html'
    context_object_name = 'tariff'
