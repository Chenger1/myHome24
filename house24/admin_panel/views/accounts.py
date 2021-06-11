from django.views.generic import CreateView, View, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.account_forms import AccountSearchForm, CreatePersonalAccountForm
from admin_panel.utils.statistic import MinimalStatisticCollector

from db.models.house import PersonalAccount
from db.services.search import PersonalAccountSearch


class ListPersonalAccountsView(ListInstancesMixin):
    model = PersonalAccount
    search_form = AccountSearchForm
    template_name = 'account/list_accounts_admin.html'
    search_obj = PersonalAccountSearch

    def get_context_data(self):
        context = super().get_context_data()
        context['statistic'] = MinimalStatisticCollector().prepare_statistic()
        return context


class CreatePersonalAccountView(AdminPermissionMixin, CreateView):
    model = PersonalAccount
    form_class = CreatePersonalAccountForm
    template_name = 'account/create_account_admin.html'
    success_url = reverse_lazy('admin_panel:list_accounts_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_number'] = self.model.get_next_account_number()
        return context


class UpdatePersonalAccountView(AdminPermissionMixin, View):
    model = PersonalAccount
    form = CreatePersonalAccountForm
    template_name = 'account/create_account_admin.html'

    def get(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        if instance.house:
            house_pk = instance.house.pk
            form = self.form(instance=instance, **{'house_pk': house_pk})
        else:
            form = self.form(instance=instance)
        context = {'form': form}
        if instance.flat and instance.flat.owner:
            owner = instance.flat.owner.full_name
            phone = instance.flat.owner.phone_number
            context.update({'owner': owner, 'phone': phone})
        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        form = self.form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:list_accounts_admin')
        return render(request, self.template_name, context={'form': form})


class DeleteAccountView(DeleteInstanceView):
    model = PersonalAccount
    redirect_url = 'admin_panel:list_accounts_admin'


class PersonalAccountDetailView(AdminPermissionMixin, DetailView):
    model = PersonalAccount
    template_name = 'account/personal_account_detail_admin.html'
    context_object_name = 'account'
