from django.views.generic import View
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from db.models.house import MasterRequest


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
