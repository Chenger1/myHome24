from django.views.generic import CreateView
from django.urls import reverse_lazy

from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.account_transaction_forms import AccountTransactionSearchForm, CreateIncomeForm

from db.models.house import Transaction


class ListAccountTransactionView(ListInstancesMixin):
    model = Transaction
    template_name = 'account_transaction/list_account_transaction_admin.html'
    search_form = AccountTransactionSearchForm

    def get_context_data(self):
        context = super().get_context_data()
        incomes = Transaction.objects.filter(payment_item_type__exact=1).count()
        outcomes = Transaction.objects.filter(payment_item_type__exact=0).count()
        context.update({'incomes': incomes,
                        'outcomes': outcomes})
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
            form = self.form_class(initial={'number': self.model.get_next_transaction_number()})
        return form
