from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import View


class ListPaginatedQuery(View):
    model = None
    template_name = None
    paginate_by = 15

    def get_paginated_query(self, query, current_page):
        paginator = Paginator(query.order_by('-pk'), self.paginate_by)
        page = current_page

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        return queryset
