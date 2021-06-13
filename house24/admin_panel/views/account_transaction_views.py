from django.views.generic import CreateView, UpdateView, DetailView, View
from django.urls import reverse_lazy
from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404, render

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.account_transaction_forms import (AccountTransactionSearchForm, CreateIncomeForm,
                                                         CreateOutcomeForm)
from admin_panel.utils.statistic import MinimalStatisticCollector

from db.models.house import Transaction, PersonalAccount
from db.services.search import TransactionSearch


class ListAccountTransactionView(ListInstancesMixin):
    model = Transaction
    template_name = 'account_transaction/list_account_transaction_admin.html'
    search_form = AccountTransactionSearchForm
    search_obj = TransactionSearch

    def get_context_data(self):
        context = super().get_context_data()
        incomes = Transaction.objects.filter(payment_item_type__type=0).aggregate(Sum('amount'))
        outcomes = Transaction.objects.filter(payment_item_type__type=1).aggregate(Sum('amount'))
        context.update({'incomes': incomes['amount__sum'],
                        'outcomes': outcomes['amount__sum']})
        context['statistic'] = MinimalStatisticCollector().prepare_statistic()
        return context


class ListAccountTransactionViewAscendingView(ListAccountTransactionView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created')
        return queryset

    def get_filtered_query(self, form_data):
        queryset = super().get_filtered_query(form_data).order_by('-created')
        return queryset


class ListAccountTransactionViewDescendingView(ListAccountTransactionView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('created')
        return queryset

    def get_filtered_query(self, form_data):
        queryset = super().get_filtered_query(form_data).order_by('created')
        return queryset


class CreateIncomeView(AdminPermissionMixin, CreateView):
    model = Transaction
    form_class = CreateIncomeForm
    template_name = 'account_transaction/create_income_admin.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin_panel:list_account_transaction_admin')
    parent_object = None

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            self.parent_object = get_object_or_404(PersonalAccount, pk=kwargs.get('pk'))
        return super().get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if self.request.POST:
            form = self.form_class(self.request.POST)
        else:
            if self.parent_object:
                form = self.form_class(initial={'number': self.model.get_next_income_number(),
                                                'owner': self.parent_object.flat.owner.pk if self.parent_object.flat.owner else None,
                                                'personal_account': self.parent_object.pk})
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


class DeleteTransactionView(DeleteInstanceView):
    model = Transaction
    redirect_url = 'admin_panel:list_account_transaction_admin'


class DetailTransactionView(AdminPermissionMixin, DetailView):
    model = Transaction
    template_name = 'account_transaction/detail_transaction_admin.html'
    context_object_name = 'transaction'


class DuplicateTransactionView(AdminPermissionMixin, View):
    model = Transaction
    form_class = None
    template_name = None
    get_text_number_callback = None
    redirect_url = 'admin_panel:list_account_transaction_admin'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=obj, initial={'number': self.get_text_number_callback()})
        return render(request, self.template_name, context={'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.pk = None
            form.save()
            return redirect(self.redirect_url)
        else:
            return render(request, self.template_name, context={'form': form})


class DuplicateIncomeView(DuplicateTransactionView):
    form_class = CreateIncomeForm
    template_name = 'account_transaction/create_income_admin.html'
    get_text_number_callback = Transaction.get_next_income_number


class DuplicateOutcomeView(DuplicateTransactionView):
    form_class = CreateOutcomeForm
    template_name = 'account_transaction/create_outcome_admin.html'
    get_text_number_callback = Transaction.get_next_outcome_number


class ListIncomeTransactionByAccount(ListInstancesMixin):
    model = Transaction
    template_name = 'account_transaction/list_account_transaction_admin.html'
    search_form = AccountTransactionSearchForm
    pk = None

    def get(self, request, pk=None):
        self.pk = pk
        return super().get(request)

    def get_queryset(self):
        return self.model.objects.filter(personal_account__pk=self.pk,
                                         payment_item_type__type=0)

    def get_context_data(self):
        context = super().get_context_data()
        incomes = self.model.objects.filter(personal_account__pk=self.pk,
                                            payment_item_type__type=0).aggregate(Sum('amount'))['amount__sum'] or 0
        outcomes = self.model.objects.filter(personal_account__pk=self.pk,
                                             payment_item_type__type=1).aggregate(Sum('amount'))['amount__sum'] or 0
        context.update({'incomes': incomes,
                        'outcomes': outcomes})
        context['statistic'] = MinimalStatisticCollector().prepare_statistic()
        return context
