from django.views.generic import View
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView, DeleteInstanceWithoutReload
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.payment_ticket_forms import PaymentTicketSearch, CreatePaymentTicketForm, TicketServiceFormset

from db.models.house import PaymentTicket, PaymentTicketService


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
        formset = TicketServiceFormset()
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


class UpdatePaymentTicketView(AdminPermissionMixin, View):
    model = PaymentTicket
    form_class = CreatePaymentTicketForm
    formset_class = TicketServiceFormset
    template_name = 'ticket/create_payment_ticket_admin.html'
    redirect_url = 'admin_panel:list_payment_ticket_admin'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=obj, **{'house_pk': obj.house.pk})
        formset = self.formset_class(instance=obj)
        return render(request, self.template_name, context={'form': form,
                                                            'formset': formset})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=obj)
        formset = self.formset_class(request.POST, instance=obj)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(self.redirect_url)
        else:
            return render(request, self.template_name, context={'form': form,
                                                                'formset': formset})


class DeleteTicketService(DeleteInstanceWithoutReload):
    model = PaymentTicketService
