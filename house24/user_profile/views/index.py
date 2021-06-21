from django.views.generic import View
from django.shortcuts import render


class IndexView(View):
    template_name = 'user_profile.html'

    def get(self, request, pk):
        return render(request, self.template_name, context={'pk': pk})
