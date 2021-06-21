from django.views.generic import View
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect


class LoginViewMixin(View):
    template_name = 'auth/admin_login.html'
    form = None
    redirect_url = None

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        else:
            form = self.form()
            return render(request, self.template_name, context={'form': form})

    def authenticate_user(self, request, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)
        return user
