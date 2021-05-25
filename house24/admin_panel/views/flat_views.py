from django.views.generic import CreateView, View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.forms.flat_forms import FlatSearchForm, CreateFlatForm
from admin_panel.permission_mixin import AdminPermissionMixin

from db.models.house import Flat, House, PersonalAccount


class ListFlatsView(ListInstancesMixin):
    model = Flat
    template_name = 'flat/list_flats_admin.html'
    search_form = FlatSearchForm


class CreateFlatView(AdminPermissionMixin, CreateView):
    model = Flat
    form_class = CreateFlatForm
    template_name = 'flat/create_flat_admin.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personal_accounts'] = PersonalAccount.objects.filter(flats=None)
        return context


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
