from django.views.generic import View
from django.shortcuts import render

from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.forms.account_forms import AccountSearchForm, CreatePersonalAccountForm

from db.models.house import PersonalAccount


class ListPersonalAccountsView(ListInstancesMixin):
    model = PersonalAccount
    search_form = AccountSearchForm
    template_name = 'account/list_accounts_admin.html'


class CreatePersonalAccountView(View):
    model = PersonalAccount
    form = CreatePersonalAccountForm
    template_name = 'account/create_account_admin.html'

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, context={'form': form})
