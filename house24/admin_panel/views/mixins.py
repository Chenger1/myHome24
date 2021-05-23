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


class ListInstancesMixin(AdminPermissionMixin, View):
    model = None
    template_name = None
    search_form = SearchForm

    def get(self, request):
        if request.GET:
            form = self.search_form(request.GET)
            if form.is_valid():
                instances = self.get_filtered_query(form.cleaned_data)
                return render(request, self.template_name, context={'form': form,
                                                                    'instances': instances})
            else:
                instances = self.get_queryset()
                return render(request, self.template_name, context={'form': form,
                                                                    'instances': instances})
        else:
            form = self.search_form()
            instances = self.get_queryset()
        return render(request, self.template_name, context={'form': form,
                                                            'instances': instances})

    def get_filtered_query(self, form_data):
        """
            Redefine if you need more specific search arguments
        """
        instances = self.model.search(form_data)
        return instances

    def get_queryset(self):
        """
            Redefine if you need more specific filtered queryset
        """
        return self.model.objects.all()
