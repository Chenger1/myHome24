from django.views.generic import View, CreateView, UpdateView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from db.models.user import Role
from db.services.search import OwnerSearch, UserSearch

from admin_panel.forms.user_forms import (RoleFormSet, CreateAdminUserForm, UpdateAdminUserForm, CreateOwnerForm,
                                          UpdateOwnerUserForm, SearchForm)
from admin_panel.views.mixins import DeleteInstanceView, ListInstancesMixin
from admin_panel.permission_mixin import AdminPermissionMixin


User = get_user_model()


class UpdateRolesView(AdminPermissionMixin, View):
    model = Role
    template_name = 'user/roles_list.html'
    redirect_url = 'admin_panel:list_roles_admin'

    def get(self, request):
        formset = RoleFormSet()
        return render(request, self.template_name, context={'roles': formset})

    def post(self, request):
        formset = RoleFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()
            return redirect('admin_panel:list_roles_admin')
        else:
            return render(request, self.template_name, context={'roles': formset})


class ListUsersView(ListInstancesMixin):
    model = User
    template_name = 'user/list_users_admin.html'
    search_form = SearchForm
    search_obj = UserSearch

    def get_queryset(self):
        return self.model.objects.filter(is_staff=True)


class CreateAdminUser(AdminPermissionMixin, CreateView):
    model = User
    form_class = CreateAdminUserForm
    template_name = 'user/create_admin_user.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin_panel:list_users_admin')


class UpdateAdminUser(AdminPermissionMixin, UpdateView):
    model = User
    form_class = UpdateAdminUserForm
    template_name = 'user/create_admin_user.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin_panel:list_users_admin')


class DeleteAdminUser(DeleteInstanceView):
    model = User
    redirect_url = 'admin_panel:list_users_admin'


class DetailAdminUser(AdminPermissionMixin, DetailView):
    model = User
    template_name = 'user/detail_admin_user.html'
    context_object_name = 'user'


class ListOwnerView(ListInstancesMixin):
    model = User
    template_name = 'owner/list_owners.html'
    search_form = SearchForm
    search_obj = OwnerSearch

    def get_queryset(self):
        return self.model.objects.filter(is_staff=False)


class ListOwnerLastNameAscendingView(ListOwnerView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-last_name')
        return queryset

    def get_filtered_query(self, form_data):
        queryset = super().get_filtered_query(form_data).order_by('-last_name')
        return queryset


class ListOwnerLastNameDescendingView(ListOwnerView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('last_name')
        return queryset

    def get_filtered_query(self, form_data):
        queryset = super().get_filtered_query(form_data).order_by('last_name')
        return queryset


class ListOwnerDateJoinedAscendingView(ListOwnerView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date_joined')
        return queryset

    def get_filtered_query(self, form_data):
        queryset = super().get_filtered_query(form_data).order_by('-date_joined')
        return queryset


class ListOwnerDateJoinedDescendingView(ListOwnerView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('date_joined')
        return queryset

    def get_filtered_query(self, form_data):
        queryset = super().get_filtered_query(form_data).order_by('date_joined')
        return queryset


class CreateOwnerUser(AdminPermissionMixin, CreateView):
    model = User
    form_class = CreateOwnerForm
    template_name = 'owner/create_owner_user.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin_panel:list_owners_admin')


class UpdateOwnerUser(AdminPermissionMixin, UpdateView):
    model = User
    form_class = UpdateOwnerUserForm
    template_name = 'owner/create_owner_user.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin_panel:list_owners_admin')


class DeleteOwnerUser(DeleteInstanceView):
    model = User
    redirect_url = 'admin_panel:list_owners_admin'


class DetailOwnerView(AdminPermissionMixin, DetailView):
    model = User
    template_name = 'owner/detail_owner_admin.html'
    context_object_name = 'user'
