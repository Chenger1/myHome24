from django.views.generic import View, CreateView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy

from db.models.house import MasterRequest

from user_profile.forms.client_forms import CreateMasterRequest


class ListClientMasterRequestView(View):
    model = MasterRequest
    template_name = 'master_requests/list_client_master_requests.html'
    paginate_by = 15

    def get(self, request, pk):
        instances = self.model.objects.filter(owner=pk)
        page = request.GET.get('page')
        return render(request, self.template_name, context={'instances': self.get_paginated_query(instances,
                                                                                                  page)})

    def get_paginated_query(self, query, current_page):
        paginator = Paginator(query, self.paginate_by)
        page = current_page

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        return queryset


class CreateClientMasterRequestView(View):
    model = MasterRequest
    template_name = 'master_requests/create_master_request_client.html'
    form = CreateMasterRequest

    def get(self, request, pk):
        form = self.form(initial={'flat': self.request.user.flats.all()})
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
