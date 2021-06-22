from django.views.generic import View, UpdateView
from django.shortcuts import render
from django.urls import reverse_lazy

from db.models.user import User

from user_profile.forms.client_forms import OwnerForm


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
