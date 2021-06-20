from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from website.forms.auth_forms import AdminLoginForm, ClientLoginForm


class LoginViewMixin(View):
    template_name = 'auth/admin_login.html'
    form = None

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, context={'form': form})

    def authenticate_user(self, request, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)
        return user


class AdminLoginView(LoginViewMixin):
    template_name = 'auth/admin_login.html'
    form = AdminLoginForm

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            try:
                user = form.authenticate_admin(request)
            except ValidationError as e:
                form.add_error('email', e.args[0])
                return render(request, self.template_name, context={'form': form})
            login(request, user)
            path = user.role.get_available_url_pattern_by_role()
            return redirect(path)
        else:
            return render(request, self.template_name, context={'form': form})


class ClientLoginView(LoginViewMixin):
    template_name = 'auth/client_login.html'
    form = ClientLoginForm

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            try:
                user = form.authenticate_client(request)
            except ValidationError as e:
                form.add_error('login_data', e.args[0])
                return render(request, self.template_name, context={'form': form})
            login(request, user)
            return redirect('website:main_page_view')
        else:
            return render(request, self.template_name, context={'form': form})
