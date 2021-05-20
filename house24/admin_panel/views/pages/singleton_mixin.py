from django.views.generic.edit import UpdateView
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect

from admin_panel.permission_mixin import AdminPermissionMixin


class SingletonUpdateView(AdminPermissionMixin, UpdateView):
    model = None
    form_class = None
    inline_form_set = None
    template_name = None
    context_object_name = 'form'
    success_url = None

    def get_object(self, queryset=None):
        return self.model.load()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = self.inline_form_set(self.request.POST,
                                                      self.request.FILES,
                                                      instance=self.object)
            context['formset'].full_clean()
        else:
            context['formset'] = self.inline_form_set(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['formset']
        response = super().form_valid(form)
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class DeleteGalleryImageMixin(AdminPermissionMixin, View):
    model = None
    redirect_url = None

    def get(self, request, pk):
        inst = get_object_or_404(self.model, pk=pk)
        inst.delete()
        return redirect(self.redirect_url)
