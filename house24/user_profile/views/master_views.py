from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404

from db.models.house import MasterRequest

from user_profile.forms.client_forms import CreateMasterRequest
from user_profile.views.mixin import ListPaginatedQuery


class ListClientMasterRequestView(ListPaginatedQuery):
    model = MasterRequest
    template_name = 'master_requests/list_client_master_requests.html'

    def get(self, request, pk):
        instances = self.model.objects.filter(owner=pk)
        page = request.GET.get('page')
        return render(request, self.template_name, context={'instances': self.get_paginated_query(instances,
                                                                                                  page)})


class CreateClientMasterRequestView(View):
    model = MasterRequest
    template_name = 'master_requests/create_master_request_client.html'
    form = CreateMasterRequest

    def get(self, request, pk):
        form = self.form()
        form.fields['flat'].queryset = request.user.flats.all()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, pk):
        form = self.form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect('user_profile:list_master_requests_client', pk=self.request.user.pk)
        else:
            return render(request, self.template_name, context={'form': form})


class DeleteMasterRequest(View):
    model = MasterRequest

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        return redirect('user_profile:list_master_requests_client', pk=self.request.user.pk)
