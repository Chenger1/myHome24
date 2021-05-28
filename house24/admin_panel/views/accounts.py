from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.forms.account_forms import AccountSearchForm

from db.models.house import PersonalAccount


class ListPersonalAccountsView(ListInstancesMixin):
    model = PersonalAccount
    search_form = AccountSearchForm
    template_name = 'account/list_accounts_admin.html'
