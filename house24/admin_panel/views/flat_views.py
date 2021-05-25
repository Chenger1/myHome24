from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.forms.flat_forms import FlatSearchForm

from db.models.house import Flat


class ListFlatsView(ListInstancesMixin):
    model = Flat
    template_name = 'flat/list_flats_admin.html'
    search_form = FlatSearchForm
