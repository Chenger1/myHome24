from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.exceptions import ValidationError

from website.forms.auth_forms import ClientLoginForm

from common.mixin import LoginViewMixin


class ClientLoginView(LoginViewMixin):
    template_name = 'auth/client_login.html'
    form = ClientLoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('user_profile:user_profile', pk=request.user.pk)
        else:
            form = self.form()
            return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            try:
                user = form.authenticate_client(request)
            except ValidationError as e:
                form.add_error('login_data', e.args[0])
                return render(request, self.template_name, context={'form': form})
            login(request, user)
            if not form.cleaned_data.get('remember_be'):
                request.session.set_expiry(0)
            return redirect('user_profile:user_profile', pk=user.pk)
        else:
            return render(request, self.template_name, context={'form': form})
