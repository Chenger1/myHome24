from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from admin_panel.views.mixins import ListInstancesMixin

from db.models.house import House

from admin_panel.forms.house_forms import HouseSearchForm, CreateHouseForm, SectionFormset, FloorFormset, UserFormset


User = get_user_model()


class ListHousesView(ListInstancesMixin):
    model = House
    template_name = 'houses/list_houses_admin.html'
    search_form = HouseSearchForm


class CreateHouseView(View):
    model = House
    template_name = 'houses/create_house_admin.html'

    def get(self, request):
        form = CreateHouseForm()
        section_formset = SectionFormset()
        floor_formset = FloorFormset()
        user_formset = UserFormset(prefix='users')

        return render(request, self.template_name, context={'form': form,
                                                            'section_formset': section_formset,
                                                            'floor_formset': floor_formset,
                                                            'user_formset': user_formset})


class GetUserRole(View):
    model = User

    def get(self, request):
        user = get_object_or_404(User, pk=request.GET.get('pk'))
        return JsonResponse({'role': user.role.name})
