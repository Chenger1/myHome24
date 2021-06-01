from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.forms.payment_ticket_forms import PaymentTicketSearch

from db.models.house import PaymentTicket


class ListPaymentTicketsView(ListInstancesMixin):
    model = PaymentTicket
    search_form = PaymentTicketSearch
    template_name = 'tickets/list_payment_tickets.html'
