from django.shortcuts import render
from django.views.generic import View

from admin_panel.permission_mixin import AdminPermissionMixin


class IndexView(AdminPermissionMixin, View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)
