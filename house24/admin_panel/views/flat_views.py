from django.views.generic import View, DetailView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.forms.flat_forms import FlatSearchForm, CreateFlatForm
from admin_panel.permission_mixin import AdminPermissionMixin

from db.models.house import Flat, House, PersonalAccount
from db.services.search import FlatSearch
from db.services.utils import generate_next_instance_number


class ListFlatsView(ListInstancesMixin):
    model = Flat
    template_name = 'flat/list_flats_admin.html'
    search_form = FlatSearchForm
    search_obj = FlatSearch


class ListFlatsViewNumberAscendingView(ListFlatsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-number')
        return queryset


class ListFlatsViewNumberDescendingView(ListFlatsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('number')
        return queryset


class ListFlatsViewHouseAscendingView(ListFlatsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-house__name')
        return queryset


class ListFlatsViewHouseDescendingView(ListFlatsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('house__name')
        return queryset


class ListFlatsViewSectionAscendingView(ListFlatsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-section__name')
        return queryset


class ListFlatsViewSectionDescendingView(ListFlatsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('section__name')
        return queryset


class ListFlatsViewFloorAscendingView(ListFlatsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-floor__name')
        return queryset


class ListFlatsViewFloorDescendingView(ListFlatsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('floor__name')
        return queryset


class ListFlatsViewOwnerAscendingView(ListFlatsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-owner__last_name')
        return queryset


class ListFlatsViewOwnerDescendingView(ListFlatsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('owner__last_name')
        return queryset


class PostInstanceMixin:
    template_name = ''
    redirect_url = None

    def save_form(self, form, request):
        if form.is_valid():
            obj = form.save()
            account_data = form.cleaned_data.get('account')
            if account_data:
                personal_account, created = PersonalAccount.objects.get_or_create(number=account_data,
                                                                                  defaults={'house': form.cleaned_data.get('house'),
                                                                                            'section': form.cleaned_data.get('section')})
                if hasattr(obj, 'account'):
                    old_account = obj.account
                    old_account.flat = None
                    old_account.house = None
                    old_account.section = None
                    old_account.floor = None
                    old_account.save()
                personal_account.flat = obj
                personal_account.save()
                return redirect(self.redirect_url)
            else:
                if 'update_flat' in request.path:
                    if hasattr(obj, 'account'):
                        old_account = obj.account
                        old_account.flat = None
                        old_account.house = None
                        old_account.section = None
                        old_account.floor = None
                        old_account.save()
                return redirect(self.redirect_url)
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
        form = self.form_class(**{'account_number': generate_next_instance_number(PersonalAccount)})
        personal_accounts = PersonalAccount.objects.filter(flat__isnull=True)
        return render(request, self.template_name, context={'form': form,
                                                            'personal_accounts': personal_accounts})

    def post(self, request):
        form = self.form_class(request.POST)
        self.redirect_url = self.get_redirect_url(request)
        return super().save_form(form, request)

    def get_redirect_url(self, request):
        trigger = int(request.POST.get('multiple'))
        if trigger:
            return 'admin_panel:create_flat_admin'
        return 'admin_panel:list_flats_admin'


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
        form = CreateFlatForm(instance=obj, **{'account_number': personal_account,
                                               'house_pk': obj.house.pk})
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
