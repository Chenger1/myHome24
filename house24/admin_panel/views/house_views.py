from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.forms.house_forms import HouseSearchForm, CreateHouseForm, SectionFormset, FloorFormset, UserFormset

from db.models.house import House


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
            section_formset.instance = floor_formset.instance = user_formset.instance = obj
            section_formset.save()
            floor_formset.save()
            user_formset.save()
            return redirect(self.redirect_url)
        else:
            return render(request, self.template_name, context={'form': form,
                                                                'section_formset': section_formset,
                                                                'floor_formset': floor_formset,
                                                                'user_formset': user_formset})


class UpdateHouseView(View):
    model = House
    template_name = 'houses/create_house_admin.html'
    redirect_url = 'admin_panel:list_houses_admin'

    def get(self, request, pk):
        inst = get_object_or_404(self.model, pk=pk)
        form = CreateHouseForm(instance=inst)
        section_formset = SectionFormset(instance=inst)
        floor_formset = FloorFormset(instance=inst)
        user_formset = UserFormset(instance=inst, prefix='users')

        return render(request, self.template_name, context={'form': form,
                                                            'section_formset': section_formset,
                                                            'floor_formset': floor_formset,
                                                            'user_formset': user_formset})

    def post(self, request, pk):
        inst = get_object_or_404(self.model, pk=pk)
        form = CreateHouseForm(request.POST, request.FILES, instance=inst)
        section_formset = SectionFormset(request.POST, instance=inst)
        floor_formset = FloorFormset(request.POST, instance=inst)
        user_formset = UserFormset(request.POST, prefix='users', instance=inst)
        if form.is_valid() and section_formset.is_valid() and floor_formset.is_valid() and user_formset.is_valid():
            form.save()
            section_formset.save()
            floor_formset.save()
            user_formset.save()
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
        try:
            role = user.role.name
        except AttributeError:
            role = 'Нет роли'
        return JsonResponse({'role': role})


class DeleteHouseInstance(DeleteInstanceView):
    model = House
    redirect_url = 'admin_panel:list_houses_admin'
