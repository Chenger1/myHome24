from admin_panel.views.mixins import ListInstancesMixin

from db.models.house import House

from admin_panel.forms.house_forms import HouseSearchForm


class ListHousesView(ListInstancesMixin):
    model = House
    template_name = 'houses/list_houses_admin.html'
    search_form = HouseSearchForm
