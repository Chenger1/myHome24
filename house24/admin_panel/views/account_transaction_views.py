from django.views.generic import CreateView, UpdateView, DetailView, View
from django.urls import reverse_lazy
from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.account_transaction_forms import (AccountTransactionSearchForm, CreateIncomeForm,
                                                         CreateOutcomeForm)
from admin_panel.utils.statistic import MinimalStatisticCollector

from db.models.house import Transaction, PersonalAccount, Flat
from db.services.search import TransactionSearch
from db.services.utils import generate_next_instance_number
from db.services.spreadsheet import TransactionSpreadSheet, ConcreteTransactionSpreadSheer

import datetime


class ListAccountTransactionView(ListInstancesMixin):
    model = Transaction
    template_name = 'account_transaction/list_account_transaction_admin.html'
    search_form = AccountTransactionSearchForm
    search_obj = TransactionSearch

    def get_context_data(self):
        context = super().get_context_data()
        incomes = self.instances.filter(payment_item_type__type=0).aggregate(Sum('paid_sum'))
        outcomes = self.instances.filter(payment_item_type__type=1).aggregate(Sum('paid_sum'))
        context.update({'incomes': incomes['paid_sum__sum'] or 0,
                        'outcomes': outcomes['paid_sum__sum'] or 0})
        context['statistic'] = MinimalStatisticCollector().prepare_statistic()
        return context


class ListAccountTransactionViewAscendingView(ListAccountTransactionView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created')
        return queryset


class ListAccountTransactionViewDescendingView(ListAccountTransactionView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('created')
        return queryset


class CreateIncomeView(AdminPermissionMixin, View):
    model = Transaction
    form_class = CreateIncomeForm
    template_name = 'account_transaction/create_income_admin.html'
    parent_model = None
    parent_object = None

    def get(self, request, pk=None):
        if pk:
            self.parent_object = self.get_parent_object(pk)
            form = self.form_class(initial=self.get_initial_dict())
        else:
            form = self.form_class(initial={'number': generate_next_instance_number(self.model)})
        return render(request, self.template_name, context={'form': form})

    def post(self, request, pk=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:list_account_transaction_admin')
        else:
            next_number = None
            if form.errors.get('number'):
                next_number = generate_next_instance_number(self.model)
            return render(request, self.template_name, context={'form': form,
                                                                'next_number': next_number})

    def get_parent_object(self, pk):
        return get_object_or_404(self.parent_model, pk=pk)

    def get_initial_dict(self):
        return {}


class CreateIncomeByAccountView(CreateIncomeView):
    parent_model = PersonalAccount

    def get_initial_dict(self):
        return {'number': generate_next_instance_number(self.model),
                'owner': self.parent_object.flat.owner.pk if self.parent_object.flat.owner else None,
                'personal_account': self.parent_object.pk}


class CreateIncomeByFlatView(CreateIncomeView):
    parent_model = Flat

    def get_initial_dict(self):
        return {'number': generate_next_instance_number(self.model),
                'owner': self.parent_object.owner.pk if self.parent_object.owner else None,
                'personal_account': self.parent_object.account.pk}


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
            form = self.form_class(initial={'number': generate_next_instance_number(self.model)})
        return form


class UpdateIncomeView(AdminPermissionMixin, UpdateView):
    model = Transaction
    form_class = CreateIncomeForm
    template_name = 'account_transaction/create_income_admin.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin_panel:list_account_transaction_admin')

    def get_form(self, form_class=None):
        if self.request.POST:
            form = self.form_class(self.request.POST, instance=self.object)
        else:
            form = self.form_class(instance=self.object)
            form.fields['number'].widget.attrs['readonly'] = 'true'
        return form


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
        form = self.form_class(instance=obj, initial={'number': generate_next_instance_number(self.model)})
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
    search_obj = TransactionSearch
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
                                            payment_item_type__type=0).aggregate(Sum('paid_sum'))['paid_sum__sum'] or 0
        outcomes = self.model.objects.filter(personal_account__pk=self.pk,
                                             payment_item_type__type=1).aggregate(Sum('paid_sum'))['paid_sum__sum'] or 0
        context.update({'incomes': incomes,
                        'outcomes': outcomes})
        context['statistic'] = MinimalStatisticCollector().prepare_statistic()
        return context


class DownloadSpreadSheet(View):
    search_form = AccountTransactionSearchForm
    search_obj = TransactionSearch
    model = Transaction

    def get(self, request):
        form = self.search_form(request.GET)
        if form.is_valid():
            instances = self.search_obj.search(form.cleaned_data, self.model.objects.all())
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename="{self.model.__name__}{datetime.date.today().strftime("%Y%m%d")}.xls"'
            constructor = TransactionSpreadSheet(self.model)
            file = constructor.create_spreadsheet(instances)
            file.save(response)
            return response
        else:
            HttpResponse()


class DownloadConcreteTransactionSpreadSheet(View):
    model = Transaction

    def get(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{self.model.__name__}{datetime.date.today().strftime("%Y%m%d")}.xls"'
        constructor = ConcreteTransactionSpreadSheer(self.model)
        file = constructor.create_spreadsheet(instance)
        file.save(response)
        return response
