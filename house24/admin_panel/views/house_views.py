from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
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
    redirect_url = 'admin_panel:list_houses_admin'

    def get(self, request):
        form = CreateHouseForm()
        section_formset = SectionFormset()
        floor_formset = FloorFormset()
        user_formset = UserFormset(prefix='users')

        return render(request, self.template_name, context={'form': form,
                                                            'section_formset': section_formset,
                                                            'floor_formset': floor_formset,
                                                            'user_formset': user_formset})

    def post(self, request):
        form = CreateHouseForm(request.POST, request.FILES)
        section_formset = SectionFormset(request.POST)
        floor_formset = FloorFormset(request.POST)
        user_formset = UserFormset(request.POST, prefix='users')
        if form.is_valid() and section_formset.is_valid() and floor_formset.is_valid() and user_formset.is_valid():
            obj = form.save()
            section_formset.instance = floor_formset.instance = obj
            section_formset.save()
            floor_formset.save()
            for user in user_formset.cleaned_data:
                #  This formset contain obj to many-to-many fields
                obj.users.add(user['user'])
            return redirect(self.redirect_url)
        else:
            return render(request, self.template_name, context={'form': form,
                                                                'section_formset': section_formset,
                                                                'floor_formset': floor_formset,
                                                                'user_formset': user_formset})


class GetUserRole(View):
    model = User

    def get(self, request):
        user = get_object_or_404(User, pk=request.GET.get('pk'))
        return JsonResponse({'role': user.role.name})
