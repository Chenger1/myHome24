from django.views.generic import View, UpdateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout, get_user_model

from user_profile.forms.client_forms import OwnerForm


User = get_user_model()


class UserProfileView(View):
    template_name = 'profile/user_profile.html'

    def get(self, request, pk):
        return render(request, self.template_name, context={'pk': pk})


class UpdateClientView(UpdateView):
    model = User
    template_name = 'profile/edit_user_client.html'
    form_class = OwnerForm

    def get_success_url(self):
        return reverse_lazy('user_profile:user_profile', args=[self.request.user.pk])


class LogoutClient(View):
    def get(self, request):
        logout(request)
        return redirect('website:main_page_view')
