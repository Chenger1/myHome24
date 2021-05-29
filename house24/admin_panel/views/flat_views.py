from django.views.generic import View, DetailView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.forms.flat_forms import FlatSearchForm, CreateFlatForm
from admin_panel.forms.account_forms import PersonalAccountForm
from admin_panel.permission_mixin import AdminPermissionMixin

from db.models.house import Flat, House, PersonalAccount


class ListFlatsView(ListInstancesMixin):
    model = Flat
    template_name = 'flat/list_flats_admin.html'
    search_form = FlatSearchForm


class PostInstanceMixin:
    template_name = ''

    def save_form(self, form, request):
        if form.is_valid():
            obj = form.save()
            account_data = form.cleaned_data.get('account')
            if account_data:
                personal_account = PersonalAccount.find_inst(account_data)
                if personal_account:
                    # if this account already exists  - set it as account for this flat
                    old_account = obj.account
                    old_account.flat = None  # clear old one-to-one field
                    old_account.save()
                    personal_account.flat = obj
                    personal_account.save()
                    return redirect('admin_panel:list_flats_admin')
                else:
                    #  otherwise - we will create new personal account using given data
                    data = {'number': form.cleaned_data['account'],
                            'house': form.cleaned_data.get('house'),
                            'section': form.cleaned_data.get('section')}
                    account_form = PersonalAccountForm(data)
                    if account_form.is_valid():
                        new_account = account_form.save()
                        new_account.flat = obj
                        new_account.save()
                        return redirect('admin_panel:list_flats_admin')
                    else:
                        obj.delete()
                        personal_accounts = PersonalAccount.objects.filter(flat__isnull=True)
                        return render(request, self.template_name, context={'form': form,
                                                                            'personal_accounts': personal_accounts})
            else:
                return redirect('admin_panel:list_flats_admin')
        else:
            personal_accounts = PersonalAccount.objects.filter(flat__isnull=True)
            return render(request, self.template_name, context={'form': form,
                                                                'personal_accounts': personal_accounts})


class CreateFlatView(AdminPermissionMixin, View, PostInstanceMixin):
    model = Flat
    form_class = CreateFlatForm
    template_name = 'flat/create_flat_admin.html'
    redirect_url = 'admin_panel:list_flats_admin'

    def get(self, request, pk=None):
        form = self.form_class()
        personal_accounts = PersonalAccount.objects.filter(flat__isnull=True)
        return render(request, self.template_name, context={'form': form,
                                                            'personal_accounts': personal_accounts})

    def post(self, request):
        form = self.form_class(request.POST)
        return super().save_form(form, request)


class UpdateFlatView(AdminPermissionMixin, View, PostInstanceMixin):
    model = Flat
    form_class = CreateFlatForm
    template_name = 'flat/create_flat_admin.html'
    redirect_url = 'admin_panel:list_flats_admin'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        try:
            personal_account = obj.account.number
        except AttributeError:
            personal_account = None
        form = CreateFlatForm(instance=obj, **{'account_number': personal_account})
        personal_accounts = PersonalAccount.objects.filter(flat__isnull=True)
        return render(request, self.template_name, context={'form': form,
                                                            'personal_accounts': personal_accounts})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = CreateFlatForm(request.POST, instance=obj)
        return super().save_form(form, request)


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


class DeleteFlatView(DeleteInstanceView):
    model = Flat
    redirect_url = 'admin_panel:list_flats_admin'


class DetailFlatView(DetailView):
    model = Flat
    template_name = 'flat/detail_flat_admin.html'
    context_object_name = 'flat'
