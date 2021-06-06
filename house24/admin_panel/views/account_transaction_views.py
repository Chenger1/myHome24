from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Sum

from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.account_transaction_forms import AccountTransactionSearchForm, CreateIncomeForm, CreateOutcomeForm

from db.models.house import Transaction


class ListAccountTransactionView(ListInstancesMixin):
    model = Transaction
    template_name = 'account_transaction/list_account_transaction_admin.html'
    search_form = AccountTransactionSearchForm

    def get_context_data(self):
        context = super().get_context_data()
        incomes = Transaction.objects.filter(payment_item_type__type=0).aggregate(Sum('amount'))
        outcomes = Transaction.objects.filter(payment_item_type__type=1).aggregate(Sum('amount'))
        context.update({'incomes': incomes['amount__sum'],
                        'outcomes': outcomes['amount__sum']})
        return context


class CreateIncomeView(AdminPermissionMixin, CreateView):
    model = Transaction
    form_class = CreateIncomeForm
    template_name = 'account_transaction/create_income_admin.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin_panel:list_account_transaction_admin')

    def get_form(self, form_class=None):
        if self.request.POST:
            form = self.form_class(self.request.POST)
        else:
            form = self.form_class(initial={'number': self.model.get_next_income_number()})
        return form


class CreateOutcomeView(AdminPermissionMixin, CreateView):
    model = Transaction
    form_class = CreateOutcomeForm
    template_name = 'account_transaction/create_outcome_admin.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin_panel:list_account_transaction_admin')

    def get_form(self, form_class=None):
        if self.request.POST:
            form = self.form_class(self.request.POST)
        else:
            form = self.form_class(initial={'number': self.model.get_next_outcome_number()})
        return form


class UpdateIncomeView(AdminPermissionMixin, UpdateView):
    model = Transaction
    form_class = CreateIncomeForm
    template_name = 'account_transaction/create_income_admin.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin_panel:list_account_transaction_admin')


class UpdateOutcomeView(AdminPermissionMixin, UpdateView):
    model = Transaction
    form_class = CreateOutcomeForm
    template_name = 'account_transaction/create_outcome_admin.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin_panel:list_account_transaction_admin')
