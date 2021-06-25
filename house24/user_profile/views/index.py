from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from db.models.house import Flat

from user_profile.services.statistic import StatisticController


class IndexView(View):
    model = Flat
    template_name = 'client_index.html'

    def get(self, request, pk):
        flat = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, context={'flat': flat})


class GetStatistic(View):
    model = Flat

    def get(self, request):
        flat = get_object_or_404(self.model, pk=request.GET.get('pk'))
        statistic = StatisticController(flat).prepare_statistic()
        return JsonResponse(statistic)
