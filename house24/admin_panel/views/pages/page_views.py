from django.views.generic.edit import UpdateView

from db.models.pages import MainPage

from admin_panel.forms.page_forms import MainPageForm, mainPageFormSet


class MainPageView(UpdateView):
    model = MainPage
    form_class = MainPageForm
    inline_form_set = mainPageFormSet
    template_name = 'pages/main_page_admin.html'
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
