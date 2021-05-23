from admin_panel.views.mixins import ListInstancesMixin

from db.models.house import House


class ListHousesView(ListInstancesMixin):
    model = House
    template_name = 'houses/list_houses_admin.html'
