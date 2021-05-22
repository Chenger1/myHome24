from django.views.generic import View
from django.shortcuts import render, redirect

from db.models.user import Role

from admin_panel.forms.user_forms import RoleFormSet


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
