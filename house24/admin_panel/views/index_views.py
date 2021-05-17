from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    template_name = 'admin_base.html'

    def get(self, request):
        return render(request, self.template_name)
