from django.views.generic import View
from django.shortcuts import render, get_object_or_404

from db.models.house import Flat


class IndexView(View):
    model = Flat
    template_name = 'client_index.html'

    def get(self, request, pk):
        flat = get_object_or_404(self.model, pk=pk)

        return render(request, self.template_name, context={'flat': flat})
