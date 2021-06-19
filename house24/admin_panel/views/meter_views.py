from django.views.generic import CreateView, View, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.meters_forms import SearchMeasureForm, CreateMeterForm, SearchMeasureHistoryForm

from db.models.house import Meter, Flat
from db.services.search import MeterSearch, MeterHistorySearch
from db.services.utils import generate_next_instance_number

import datetime


class ListMetersView(ListInstancesMixin):
    model = Meter
    search_form = SearchMeasureForm
    template_name = 'meters/list_meters_admin.html'
    search_obj = MeterSearch


class ListMetersNumberAscendingView(ListMetersView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-flat__number')
        return queryset


class ListMetersNumberDescendingView(ListMetersView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('flat__number')
        return queryset


class CreateMeterView(AdminPermissionMixin, CreateView):
    model = Meter
    form_class = CreateMeterForm
    template_name = 'meters/create_meter_admin.html'
    flat = None

    def get(self, request, *args, **kwargs):
        self.flat = kwargs.get('pk')
        return super().get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if self.request.POST:
            form = self.form_class(self.request.POST)
        else:
            if self.flat:
                flat = get_object_or_404(Flat, pk=self.flat)
                form = self.form_class(initial={'house': flat.house,
                                                'section': flat.section,
                                                'flat': flat})
            else:
                form = self.form_class()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_number'] = generate_next_instance_number(self.model)
        return context

    def get_success_url(self):
        trigger = int(self.request.POST.get('multiple'))
        if trigger:
            return reverse_lazy('admin_panel:create_meter_admin')
        return reverse_lazy('admin_panel:list_meter_history', args=[self.object.flat.pk])


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
    search_obj = MeterHistorySearch
    pk = None

    def get(self, request, pk=None):
        self.pk = pk
        return super().get(request)

    def get_queryset(self):
        return self.model.objects.filter(flat__pk=self.pk)

    def get_context_data(self):
        context = super().get_context_data()
        context['flat'] = get_object_or_404(Flat, pk=self.pk)
        return context


class ListMeterHistoryDateAscending(ListMeterHistory):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date')
        return queryset


class ListMeterHistoryDateDescending(ListMeterHistory):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('date')
        return queryset


class ListMeterHistoryMonthAscending(ListMeterHistory):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date__month')
        return queryset


class ListMeterHistoryMonthDescending(ListMeterHistory):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date__month')
        return queryset


class MeterDetailView(AdminPermissionMixin, DetailView):
    model = Meter
    template_name = 'meters/meter_detail_admin.html'
    context_object_name = 'meter'


class DeleteMeterView(DeleteInstanceView):
    model = Meter
    redirect_url = 'admin_panel:list_meters_admin'

    def get(self, request, pk, flat_pk=None):
        if flat_pk:
            self.redirect_url = reverse_lazy('admin_panel:list_meter_history', args=[flat_pk])
        return super().get(request, pk)


class DuplicateMeterView(AdminPermissionMixin, View):
    model = Meter
    form = CreateMeterForm
    template_name = 'meters/create_meter_admin.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form(instance=obj, initial={'number': generate_next_instance_number(self.model),
                                                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                                                'status': 0, 'data': ''})
        form.instance.number = generate_next_instance_number(self.model)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, pk):
        form = self.form(request.POST)
        if form.is_valid():
            form.instance.pk = None
            form.save()
            return redirect('admin_panel:list_meters_admin')
        else:
            return render(request, self.template_name, context={'form': form})
