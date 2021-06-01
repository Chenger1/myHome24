from django.views.generic import View
from django.shortcuts import render

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

    def get(self, request):
        form = CreatePaymentTicketForm()
        formset = TicketServiceFormset
        next_number = self.model.get_next_ticket_number()
        meters = Meter.objects.all()
        return render(request, self.template_name, context={'form': form,
                                                            'formset': formset,
                                                            'next_number': next_number,
                                                            'meters': meters})
