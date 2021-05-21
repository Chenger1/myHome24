from django.views.generic.list import ListView

from db.models.house import Tariff


class ListTariff(ListView):
    model = Tariff
    template_name = 'options/tariff_list.html'
    context_object_name = 'tariffs'
