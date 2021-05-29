from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect

from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.meters_forms import SearchMeasureForm, CreateMeterForm

from db.models.house import Meter


class ListMetersView(ListInstancesMixin):
    model = Meter
    search_form = SearchMeasureForm
    template_name = 'meters/list_meters_admin.html'


class CreateMeterView(AdminPermissionMixin, CreateView):
    model = Meter
    form_class = CreateMeterForm
    template_name = 'meters/create_meter_admin.html'
    success_url = reverse_lazy('admin_panel:list_meters_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_number'] = self.model.get_next_meter_number()
        return context


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
