from django.views.generic import CreateView
from django.urls import reverse_lazy

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.account_forms import AccountSearchForm, CreatePersonalAccountForm

from db.models.house import PersonalAccount


class ListPersonalAccountsView(ListInstancesMixin):
    model = PersonalAccount
    search_form = AccountSearchForm
    template_name = 'account/list_accounts_admin.html'


class CreatePersonalAccountView(AdminPermissionMixin, CreateView):
    model = PersonalAccount
    form_class = CreatePersonalAccountForm
    template_name = 'account/create_account_admin.html'
    success_url = reverse_lazy('admin_panel:list_accounts_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_number'] = self.model.get_next_account_number()
        return context


class DeleteAccountView(DeleteInstanceView):
    model = PersonalAccount
    redirect_url = 'admin_panel:list_accounts_admin'
