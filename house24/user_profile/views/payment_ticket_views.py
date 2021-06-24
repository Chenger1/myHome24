from django.shortcuts import render, get_object_or_404

from user_profile.views.mixin import ListPaginatedQuery
from user_profile.forms.client_forms import SearchTicketsForm

from db.models.house import Flat, PaymentTicket


class ListPaymentTicketsByFlatView(ListPaginatedQuery):
    model = Flat
    template_name = 'payment_tickets/list_payment_tickets_user.html'
    search_form = SearchTicketsForm

    def get(self, request, pk):
        flat = get_object_or_404(self.model, pk=pk)
        page = request.GET.get('page')
        form = self.search_form(request.GET)
        instances = flat.tickets.all()
        if form.is_valid():
            if form.cleaned_data.get('start'):
                instances = instances.filter(start=form.cleaned_data.get('start'))
            if form.cleaned_data.get('status'):
                instances = instances.filter(status=form.cleaned_data.get('status'))
        else:
            instances = flat.tickets.all().order_by('-pk')
        return render(request, self.template_name, context={'instances': self.get_paginated_query(instances, page),
                                                            'flat': flat,
                                                            'form': form})


class ListPaymentTicketsView(ListPaginatedQuery):
    model = PaymentTicket
    template_name = 'payment_tickets/list_payment_tickets_user.html'
    search_form = SearchTicketsForm

    def get(self, request, pk):
        instances = PaymentTicket.objects.filter(flat__owner__pk=pk)
        page = request.GET.get('page')
        form = self.search_form(request.GET)
        if form.is_valid():
            if form.cleaned_data.get('start'):
                instances = instances.filter(start=form.cleaned_data.get('start'))
            if form.cleaned_data.get('status'):
                instances = instances.filter(status=form.cleaned_data.get('status'))
        else:
            instances = instances.order_by('-pk')
        return render(request, self.template_name, context={'instances': self.get_paginated_query(instances, page),
                                                            'form': form})
