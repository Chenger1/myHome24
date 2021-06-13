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
    search_obj = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instances = None
        self.form = None

    def get(self, request, pk=None):
        self.form = self.search_form(request.GET)
        if self.form.is_valid():
            self.instances = self.get_filtered_query(self.form.cleaned_data)
            return render(request, self.template_name, context=self.get_context_data())
        else:
            self.instances = self.get_queryset()[::-1]
            return render(request, self.template_name, context=self.get_context_data())

    def get_filtered_query(self, form_data):
        """
            Redefine if you need more specific search arguments
        """
        instances = self.search_obj.search(form_data, self.get_queryset())
        return instances.order_by('-pk')

    def get_queryset(self):
        """
            Redefine if you need more specific filtered queryset
        """
        return self.model.objects.all()

    def get_context_data(self):
        """
            Redefine if you need to add additional context variables
        """
        context = {'form': self.form,
                   'instances': self.instances,
                   'count': len(self.instances)}
        return context


class FlatOwner(View):
    model = Flat

    def get(self, request):
        if not request.GET.get('pk'):
            return JsonResponse({})
        flat = get_object_or_404(self.model, pk=request.GET.get('pk'))
        if flat.owner:
            owner = {'full_name': flat.owner.full_name,
                     'phone': flat.owner.phone_number}
            return JsonResponse(owner)
        else:
            return JsonResponse({})
