from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.forms.meters_forms import SearchMeasureForm

from db.models.house import Meter


class ListMetersView(ListInstancesMixin):
    model = Meter
    search_form = SearchMeasureForm
    template_name = 'meters/list_meters_admin.html'
