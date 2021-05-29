from django.views.generic import CreateView
from django.urls import reverse_lazy

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
