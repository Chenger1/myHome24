from django.views.generic import View
from django.shortcuts import redirect, get_object_or_404, render
from django.http import JsonResponse

from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.user_forms import SearchForm

from db.models.house import Flat


class DeleteInstanceView(AdminPermissionMixin, View):
    model = None
    redirect_url = None

    def get(self, request, pk):
        inst = get_object_or_404(self.model, pk=pk)
        inst.delete()
        return redirect(self.redirect_url)


class DeleteInstanceWithoutReload(AdminPermissionMixin, View):
    model = None

    def get(self, request):
        inst = get_object_or_404(self.model, pk=request.GET.get('pk'))
        inst.delete()
        return JsonResponse({'status': 200})


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
        return instances[::-1]

    def get_queryset(self):
        """
            Redefine if you need more specific filtered queryset
        """
        return self.model.objects.all()[::-1]


class FlatOwner(View):
    model = Flat

    def get(self, request):
        flat = get_object_or_404(self.model, pk=request.GET.get('pk'))
        owner = dict()
        if flat.owner:
            owner = {'full_name': flat.owner.full_name,
                     'phone': flat.owner.phone_number}
        return JsonResponse(owner)
