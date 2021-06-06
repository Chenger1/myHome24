from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.forms.account_transaction_forms import AccountTransactionSearchForm

from db.models.house import Transfer


class ListAccountTransactionView(ListInstancesMixin):
    model = Transfer
    template_name = 'account_transaction/list_account_transaction_admin.html'
    search_form = AccountTransactionSearchForm
