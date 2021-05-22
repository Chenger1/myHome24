from django.views.generic import View, ListView
from django.shortcuts import render, redirect

from db.models.user import Role, User

from admin_panel.forms.user_forms import RoleFormSet, SearchForm


class UpdateRolesView(View):
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


class ListUsersView(View):
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

