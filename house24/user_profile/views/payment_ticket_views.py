from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View
from django.contrib.auth import get_user_model
from django.contrib import messages

from user_profile.views.mixin import ListPaginatedQuery
from user_profile.forms.client_forms import SearchTicketsForm, CreateTransaction

from db.models.house import Flat, PaymentTicket, Transaction, PaymentItem
from db.services.utils import generate_next_instance_number


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


class PaymentTicketDetailClintView(DetailView):
    model = PaymentTicket
    template_name = 'payment_tickets/detail_payment_ticket_client.html'
    context_object_name = 'ticket'


class PrintPaymentTicketView(View):
    model = PaymentTicket
    template_name = 'ticket_print_template.html'

    def get(self, request, pk):
        ticket = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, context={'ticket': ticket})


class CreateTransactionByTicket(View):
    model = Transaction
    template_name = 'payment_tickets/create_ticket_transaction.html'
    form = CreateTransaction

    def get(self, request, pk):
        ticket = get_object_or_404(PaymentTicket, pk=pk)
        form = self.form(initial={'number': generate_next_instance_number(self.model),
                                  'owner': request.user,
                                  'personal_account': ticket.personal_account,
                                  'payment_ticket': ticket,
                                  'payment_item_type': PaymentItem.objects.get(default_income_type=True)})
        return render(request, self.template_name, context={'form': form,
                                                            'ticket': ticket})

    def post(self, request, pk):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Ваша оплата отправлена на подтверждение')
            return redirect('user_profile:list_payment_tickets_client', pk=request.user.pk)
        else:
            ticket = get_object_or_404(PaymentTicket, pk=pk)
            return render(request, self.template_name, context={'form': form,
                                                                'ticket': ticket})
