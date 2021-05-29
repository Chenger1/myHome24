from django.views.generic import View
from django.shortcuts import render, redirect

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.account_forms import AccountSearchForm, CreatePersonalAccountForm

from db.models.house import PersonalAccount


class ListPersonalAccountsView(ListInstancesMixin):
    model = PersonalAccount
    search_form = AccountSearchForm
    template_name = 'account/list_accounts_admin.html'


class CreatePersonalAccountView(AdminPermissionMixin, View):
    model = PersonalAccount
    form = CreatePersonalAccountForm
    template_name = 'account/create_account_admin.html'

    def get(self, request):
        form = self.form()
        next_number = self.model.get_next_account_number()
        return render(request, self.template_name, context={'form': form,
                                                            'next_number': next_number})

    def post(self, request):
        form = self.form(request.POST)
        next_number = self.model.get_next_account_number()
        if form.is_valid():
            form.save()
            return redirect('admin_panel:list_accounts_admin')
        return render(request, self.template_name, context={'form': form,
                                                            'next_number': next_number})


class DeleteAccountView(DeleteInstanceView):
    model = PersonalAccount
    redirect_url = 'admin_panel:list_accounts_admin'
