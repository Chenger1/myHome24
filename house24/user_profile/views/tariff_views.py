from django.views.generic import View
from django.shortcuts import get_object_or_404, render

from db.models.house import Flat


class ListTariffView(View):
    model = Flat
    template_name = 'client_tariff/list_client_tariff.html'

    def get(self, request, pk):
        flat = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, context={'tariff': flat.tariff,
                                                            'flat': flat})
