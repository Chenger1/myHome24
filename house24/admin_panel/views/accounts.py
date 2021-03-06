from django.views.generic import View, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.account_forms import AccountSearchForm, CreatePersonalAccountForm
from admin_panel.utils.statistic import MinimalStatisticCollector

from db.models.house import PersonalAccount, Flat, Section, Floor, House
from db.services.search import PersonalAccountSearch
from db.services.utils import generate_next_instance_number
from db.services.spreadsheet import AccountSpreadSheet

import datetime


class ListPersonalAccountsView(ListInstancesMixin):
    model = PersonalAccount
    search_form = AccountSearchForm
    template_name = 'account/list_accounts_admin.html'
    search_obj = PersonalAccountSearch

    def get_context_data(self):
        context = super().get_context_data()
        context['statistic'] = MinimalStatisticCollector().prepare_statistic()
        return context


class CreatePersonalAccountView(AdminPermissionMixin, View):
    model = PersonalAccount
    form_class = CreatePersonalAccountForm
    template_name = 'account/create_account_admin.html'

    def get(self, request):
        form = self.form_class(initial={'number': generate_next_instance_number(self.model)})
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:list_accounts_admin')
        else:
            next_number = None
            if form.errors.get('number'):
                next_number = generate_next_instance_number(self.model)
            return render(request, self.template_name, context={'form': form,
                                                                'next_number': next_number})


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
        form.fields['number'].widget.attrs['readonly'] = 'true'
        if instance.flat:
            section_queryset = instance.flat.house.sections.all()
            floor_queryset = instance.flat.section.floors.all()
            form.fields['section'].queryset = section_queryset
            form.fields['floor'].queryset = floor_queryset
            form.fields['floor'].initial = instance.flat.floor
            queryset = Flat.objects.filter(pk=instance.flat.pk) | Flat.objects.filter(account__isnull=True)
        else:
            form.fields['house'].queryset = House.objects.all()
            form.fields['house'].initial = None
            form.fields['section'].queryset = Section.objects.none()
            form.fields['floor'].queryset = Floor.objects.none()
            queryset = Flat.objects.filter(account__isnull=True)
        form.fields['flat'].queryset = queryset
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


class DownloadSpreadSheet(View):
    search_form = AccountSearchForm
    search_obj = PersonalAccountSearch
    model = PersonalAccount

    def get(self, request):
        form = self.search_form(request.GET)
        if form.is_valid():
            instances = self.search_obj.search(form.cleaned_data, self.model.objects.all())
            response = HttpResponse(content_type='application/ms-excel')
            time_now = datetime.date.today().strftime("%Y%m%d")
            response['Content-Disposition'] = f'attachment; filename="{self.model.__name__}{time_now}.xls"'
            constructor = AccountSpreadSheet(self.model)
            file = constructor.create_spreadsheet(instances)
            file.save(response)
            return response
        else:
            HttpResponse()
