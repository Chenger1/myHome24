from django.views.generic import View, CreateView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from db.models.user import Role

from admin_panel.forms.user_forms import RoleFormSet, SearchForm, CreateAdminUserForm, UpdateAdminUserForm
from admin_panel.views.mixins import DeleteInstanceView
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


class ListUsersView(AdminPermissionMixin, View):
    model = User
    template_name = 'user/list_users_admin.html'
    context_object_name = 'users'

    def get(self, request):
        if request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                users = self.model.search(form.cleaned_data)
                return render(request, self.template_name, context={'form': form,
                                                                    'users': users})
            else:
                users = self.model.objects.filter(is_staff=True)
                return render(request, self.template_name, context={'form': form,
                                                                    'users': users})
        else:
            form = SearchForm()
            users = self.model.objects.filter(is_staff=True)
        return render(request, self.template_name, context={'form': form,
                                                            'users': users})


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
