from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import logout
from django.shortcuts import redirect

from admin_panel.permission_mixin import AdminPermissionMixin


class IndexView(AdminPermissionMixin, View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)


class LogoutAdmin(AdminPermissionMixin, View):
    def get(self, request):
        logout(request)
        return redirect('website:main_page_view')
