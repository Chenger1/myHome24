from django.views.generic import View
from django.shortcuts import redirect, get_object_or_404, render

from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.user_forms import SearchForm


class DeleteInstanceView(AdminPermissionMixin, View):
    model = None
    redirect_url = None

    def get(self, request, pk):
        inst = get_object_or_404(self.model, pk=pk)
        inst.delete()
        return redirect(self.redirect_url)


class ListUsersViewMixin(AdminPermissionMixin, View):
    model = None
    template_name = None
    context_object_name = 'users'
    search_form = SearchForm
    is_staff = None

    def get(self, request):
        if request.GET:
            form = self.search_form(request.GET)
            if form.is_valid():
                users = self.model.search(form.cleaned_data, self.is_staff)
                return render(request, self.template_name, context={'form': form,
                                                                    'users': users})
            else:
                users = self.model.objects.filter(is_staff=self.is_staff)
                return render(request, self.template_name, context={'form': form,
                                                                    'users': users})
        else:
            form = self.search_form()
            users = self.model.objects.filter(is_staff=self.is_staff)
        return render(request, self.template_name, context={'form': form,
                                                            'users': users})
