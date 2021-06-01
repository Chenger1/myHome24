from django.views.generic import CreateView, View, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.meters_forms import SearchMeasureForm, CreateMeterForm, SearchMeasureHistoryForm

from db.models.house import Meter, Flat

import datetime


class ListMetersView(ListInstancesMixin):
    model = Meter
    search_form = SearchMeasureForm
    template_name = 'meters/list_meters_admin.html'


class CreateMeterView(AdminPermissionMixin, CreateView):
    model = Meter
    form_class = CreateMeterForm
    template_name = 'meters/create_meter_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_number'] = self.model.get_next_meter_number()
        return context

    def get_success_url(self):
        trigger = int(self.request.POST.get('multiple'))
        if trigger:
            return reverse_lazy('admin_panel:create_meter_admin')
        return reverse_lazy('admin_panel:list_meters_admin')


class UpdateMeterView(AdminPermissionMixin, View):
    model = Meter
    form = CreateMeterForm
    template_name = 'meters/create_meter_admin.html'

    def get(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        if instance.house:
            house_pk = instance.house.pk
            form = self.form(instance=instance, **{'house_pk': house_pk})
        else:
            form = self.form(instance=instance)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        form = self.form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:list_meters_admin')
        return render(request, self.template_name, context={'form': form})


class ListMeterHistory(ListInstancesMixin):
    model = Meter
    template_name = 'meters/list_meter_history.html'
    search_form = SearchMeasureHistoryForm

    def get(self, request, pk):
        self.pk = pk
        return super().get(request)

    def get_queryset(self):
        return self.model.objects.filter(flat__pk=self.pk)

    def get_context_data(self):
        context = super().get_context_data()
        context['flat'] = get_object_or_404(Flat, pk=self.pk)
        return context


class MeterDetailView(AdminPermissionMixin, DetailView):
    model = Meter
    template_name = 'meters/meter_detail_admin.html'
    context_object_name = 'meter'


class DeleteMeterView(DeleteInstanceView):
    model = Meter
    redirect_url = 'admin_panel:list_meters_admin'


class DuplicateMeterView(AdminPermissionMixin, View):
    model = Meter
    form = CreateMeterForm
    template_name = 'meters/create_meter_admin.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form(instance=obj, initial={'number': self.model.get_next_meter_number(),
                                                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                                                'status': 0, 'data': ''})
        form.instance.number = self.model.get_next_meter_number()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, pk):
        form = self.form(request.POST)
        if form.is_valid():
            form.instance.pk = None
            form.save()
            return redirect('admin_panel:list_meters_admin')
        else:
            return render(request, self.template_name, context={'form': form})
