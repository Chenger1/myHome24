from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.forms.account_transaction_forms import AccountTransactionSearchForm

from db.models.house import Transfer


class ListAccountTransactionView(ListInstancesMixin):
    model = Transfer
    template_name = 'account-transaction/list_account-transaction_admin.html'
    search_form = AccountTransactionSearchForm
