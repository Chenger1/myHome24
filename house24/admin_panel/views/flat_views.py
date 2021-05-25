from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.forms.flat_forms import FlatSearchForm, CreateFlatForm
from admin_panel.forms.account_forms import PersonalAccountForm
from admin_panel.permission_mixin import AdminPermissionMixin

from db.models.house import Flat, House, PersonalAccount


class ListFlatsView(ListInstancesMixin):
    model = Flat
    template_name = 'flat/list_flats_admin.html'
    search_form = FlatSearchForm


class CreateFlatView(AdminPermissionMixin, View):
    model = Flat
    form_class = CreateFlatForm
    template_name = 'flat/create_flat_admin.html'
    redirect_url = 'admin_panel:list_flats_admin'

    def get(self, request):
        form = CreateFlatForm()
        personal_accounts = PersonalAccount.objects.filter(flats__isnull=False)
        return render(request, self.template_name, context={'form': form,
                                                            'personal_accounts': personal_accounts})

    def post(self, request):
        form = CreateFlatForm(request.POST)
        if form.is_valid():
            obj = form.save()
            personal_account = PersonalAccount.find_inst(form.cleaned_data['personal_account'])
            if personal_account:
                # if this account already exists  - set it as account for this flat
                obj.personal_account = personal_account
            else:
                #  otherwise - we will create new personal account using given data
                data = {'number': form.cleaned_data['account'],
                        'house': form.cleaned_data['house'],
                        'section': form.cleaned_data['section']}
                account_form = PersonalAccountForm(data)
                if account_form.is_valid():
                    obj.personal_account = account_form.save()
                    return redirect('admin_panel:list_flats_admin')
                else:
                    obj.delete()
                    personal_accounts = PersonalAccount.objects.filter(flats__isnull=False)
                    return render(request, self.template_name, context={'form': form,
                                                                        'personal_accounts': personal_accounts,
                                                                        'account_errors':account_form.errors})
        else:
            personal_accounts = PersonalAccount.objects.filter(flats__isnull=False)
            return render(request, self.template_name, context={'form': form,
                                                                'personal_accounts': personal_accounts})


class GetHouseSectionAndFloor(View):
    model = House

    def get(self, request):
        house = get_object_or_404(self.model, pk=request.GET.get('pk'))
        sections = house.sections.all()
        floors = house.floors.all()
        response = {'sections': self.serialize_data(sections),
                    'floors': self.serialize_data(floors)}
        return JsonResponse(response)

    def serialize_data(self, query):
        result = {}
        for index, inst in enumerate(query):
            result.update({index: {'pk': inst.pk,
                                   'name': inst.name}})
        return result
