from django.views.generic import View, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.forms.house_forms import (HouseSearchForm, CreateHouseForm, SectionFormset, UserFormset,
                                           FloorFormset, create_floor_formset)
from admin_panel.permission_mixin import AdminPermissionMixin

from db.models.house import House, Floor, Section
from db.services.search import HouseSearch


User = get_user_model()


class ListHousesView(ListInstancesMixin):
    model = House
    template_name = 'houses/list_houses_admin.html'
    search_form = HouseSearchForm
    search_obj = HouseSearch


class ListHouseNameAscendingView(ListHousesView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-name')
        return queryset


class ListHouseNameDescendingView(ListHousesView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        return queryset


class ListHouseAddressAscendingView(ListHousesView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-address')
        return queryset


class ListHouseAddressDescendingView(ListHousesView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('address')
        return queryset


class CreateHouseView(AdminPermissionMixin, View):
    model = House
    template_name = 'houses/create_house_admin.html'
    redirect_url = 'admin_panel:update_house_admin'

    def get(self, request):
        form = CreateHouseForm()
        section_formset = SectionFormset()
        user_formset = UserFormset(prefix='users')
        return render(request, self.template_name, context={'form': form,
                                                            'section_formset': section_formset,
                                                            'user_formset': user_formset})

    def post(self, request):
        form = CreateHouseForm(request.POST, request.FILES)
        section_formset = SectionFormset(request.POST)
        user_formset = UserFormset(request.POST, prefix='users')
        if form.is_valid() and section_formset.is_valid() and user_formset.is_valid():
            obj = form.save()
            section_formset.instance = user_formset.instance = obj
            section_formset.save()
            user_formset.save()
            return redirect(self.redirect_url, pk=obj.pk)
        else:
            return render(request, self.template_name, context={'form': form,
                                                                'section_formset': section_formset,
                                                                'user_formset': user_formset})


class UpdateHouseView(AdminPermissionMixin, View):
    model = House
    template_name = 'houses/create_house_admin.html'
    redirect_url = 'admin_panel:list_houses_admin'

    def get(self, request, pk):
        inst = get_object_or_404(self.model, pk=pk)
        form = CreateHouseForm(instance=inst)
        section_formset = SectionFormset(instance=inst)
        section_queryset = Section.objects.filter(house=inst)
        floor_queryset = Floor.objects.filter(section__in=section_queryset)
        floor_formset = create_floor_formset(floor_queryset=floor_queryset,
                                             section_queryset=section_queryset)
        user_formset = UserFormset(instance=inst, prefix='users')

        return render(request, self.template_name, context={'form': form,
                                                            'section_formset': section_formset,
                                                            'floor_formset': floor_formset,
                                                            'user_formset': user_formset})

    def post(self, request, pk):
        inst = get_object_or_404(self.model, pk=pk)
        form = CreateHouseForm(request.POST, request.FILES, instance=inst)
        section_formset = SectionFormset(request.POST, instance=inst)
        floor_formset = FloorFormset(request.POST, prefix='floors')
        user_formset = UserFormset(request.POST, prefix='users', instance=inst)
        if form.is_valid() and section_formset.is_valid() and floor_formset.is_valid() and user_formset.is_valid():
            form.save()
            section_formset.save()
            user_formset.save()
            for floor_form in floor_formset.forms:
                if floor_form.cleaned_data.get('name'):
                    if floor_form.cleaned_data['DELETE']:
                        #  If we delete floor from house at all  we have to find all similar floors in this house
                        #  and delete them all
                        floors = Floor.objects.filter(section__in=floor_form.cleaned_data['sections'],
                                                      name=floor_form.cleaned_data['name'], section__house=inst)
                        floors.delete()
                        continue
                    for section in floor_form.cleaned_data['sections']:
                        #  if floor already exists in section - get, otherwise - create
                        floor, is_created = Floor.objects.get_or_create(name=floor_form.cleaned_data['name'],
                                                                        section=section)
                    floors = Floor.objects.filter(section__in=inst.sections.all(), name=floor_form.cleaned_data['name'])\
                        .exclude(section__in=floor_form.cleaned_data['sections'])
                    floors.delete()
                # if there are no section in form cleaned data - section doesnt contains this floor anymore

            return redirect(self.redirect_url)
        else:
            return render(request, self.template_name, context={'form': form,
                                                                'section_formset': section_formset,
                                                                'floor_formset': floor_formset,
                                                                'user_formset': user_formset})


class GetUserRole(AdminPermissionMixin, View):
    model = User

    def get(self, request):
        user = get_object_or_404(User, pk=request.GET.get('pk'))
        try:
            role = user.role.name
        except AttributeError:
            role = 'Нет роли'
        return JsonResponse({'role': role})


class DetailHouseView(DetailView):
    model = House
    template_name = 'houses/detail_house_admin.html'
    context_object_name = 'house'


class DeleteHouseInstance(DeleteInstanceView):
    model = House
    redirect_url = 'admin_panel:list_houses_admin'
