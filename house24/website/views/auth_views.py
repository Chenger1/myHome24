from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from website.forms.auth_forms import LoginForm


class LoginViewMixin(View):
    template_name = 'auth/admin_login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, context={'form': form})

    def authenticate_user(self, request, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)
        return user


class AdminLoginView(LoginViewMixin):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = form.authenticate_admin(request)
            except ValidationError as e:
                form.add_error('email', e.args[0])
                return render(request, self.template_name, context={'form': form})
            login(request, user)
            return redirect('admin_panel:index')
        else:
            return render(request, self.template_name, context={'form': form})

