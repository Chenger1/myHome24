from django.views.generic import View
from django.shortcuts import render, redirect

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.payment_ticket_forms import PaymentTicketSearch, CreatePaymentTicketForm, TicketServiceFormset

from db.models.house import PaymentTicket, Meter


class ListPaymentTicketsView(ListInstancesMixin):
    model = PaymentTicket
    search_form = PaymentTicketSearch
    template_name = 'ticket/list_payment_tickets.html'


class CreatePaymentTicketView(AdminPermissionMixin, View):
    model = PaymentTicket
    template_name = 'ticket/create_payment_ticket_admin.html'
    redirect_url = 'admin_panel:list_payment_ticket_admin'

    def get(self, request):
        form = CreatePaymentTicketForm()
        formset = TicketServiceFormset
        next_number = self.model.get_next_ticket_number()
        return render(request, self.template_name, context={'form': form,
                                                            'formset': formset,
                                                            'next_number': next_number})

    def post(self, request):
        form = CreatePaymentTicketForm(request.POST)
        formset = TicketServiceFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            obj = form.save()
            formset.instance = obj
            formset.save()
            return redirect(self.redirect_url)
        else:
            return render(request, self.template_name, context={'form': form,
                                                                'formset': formset})


class DeletePaymentTicketView(DeleteInstanceView):
    model = PaymentTicket
    redirect_url = 'admin_panel:list_payment_ticket_admin'
