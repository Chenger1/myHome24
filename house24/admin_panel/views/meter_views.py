from django.views.generic import CreateView

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
