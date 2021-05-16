from django.views.generic import View
from django.shortcuts import render

from website.forms.auth_forms import AdminLoginForm


class AdminLoginView(View):
    template_name = 'auth/admin_login.html'

    def get(self, request):
        form = AdminLoginForm()
        return render(request, self.template_name, context={'form': form})
