from django.views.generic import View
from django.shortcuts import render, redirect

from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.forms.payment_ticket_forms import PaymentTicketSearch, CreatePaymentTicketForm, TicketServiceFormset

from db.models.house import PaymentTicket, Meter


class ListPaymentTicketsView(ListInstancesMixin):
    model = PaymentTicket
    search_form = PaymentTicketSearch
    template_name = 'ticket/list_payment_tickets.html'


class CreatePaymentTicketView(View):
    model = PaymentTicket
    template_name = 'ticket/create_payment_ticket_admin.html'
    redirect_url = 'admin_panel:list_payment_ticket_admin'

    def get(self, request):
        form = CreatePaymentTicketForm()
        formset = TicketServiceFormset
        next_number = self.model.get_next_ticket_number()
        meters = Meter.objects.all()
        return render(request, self.template_name, context={'form': form,
                                                            'formset': formset,
                                                            'next_number': next_number,
                                                            'meters': meters})

    def post(self, request):
        form = CreatePaymentTicketForm(request.POST)
        formset = TicketServiceFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            obj = form.save()
            formset.instance = obj
            formset.save()
            return redirect(self.redirect_url)
        else:
            meters = Meter.objects.all()
            return render(request, self.template_name, context={'form': form,
                                                                'formset': formset,
                                                                'meters': meters})
