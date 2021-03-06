from django.views.generic.edit import UpdateView

from db.models.pages import (MainPage, AboutPage, ServicesPage, ContactsPage)

from admin_panel.forms.page_forms import (MainPageForm, MainPageFormSet, AboutPageForm, AboutPageGalleryInlineFormset,
                                          AboutPageAdditionalGalleryInlineFormset, DocumentsFormset,
                                          ServicesForm, ServicesBlockFormset, ContactsPageForm)

from admin_panel.views.pages.singleton_mixin import SingletonUpdateView
from admin_panel.permission_mixin import AdminPermissionMixin


class MainPageView(SingletonUpdateView):
    model = MainPage
    form_class = MainPageForm
    inline_form_set = MainPageFormSet
    template_name = 'pages/main_page_admin.html'
    context_object_name = 'form'
    success_url = None


class AboutPageView(SingletonUpdateView):
    model = AboutPage
    form_class = AboutPageForm
    inline_form_set = AboutPageGalleryInlineFormset
    inline_additional_form_set = AboutPageAdditionalGalleryInlineFormset
    documents_form_set = DocumentsFormset
    template_name = 'pages/about_page_admin.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['additional_formset'] = self.inline_additional_form_set(self.request.POST,
                                                                            self.request.FILES,
                                                                            instance=self.object)
            context['additional_formset'].full_clean()
            context['documents_formset'] = self.documents_form_set(self.request.POST,
                                                                   self.request.FILES,
                                                                   instance=self.object)
        else:
            context['additional_formset'] = self.inline_additional_form_set(instance=self.object)
            context['documents_formset'] = self.documents_form_set(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        additional_formset = context['additional_formset']
        documents_formset = context['documents_formset']
        response = super().form_valid(form)
        if additional_formset.is_valid() and documents_formset.is_valid():
            additional_formset.instance = documents_formset.instance = self.object
            additional_formset.save()
            documents_formset.save()
            return response
        else:
            return super().form_invalid(form)


class ServicesPageView(SingletonUpdateView):
    model = ServicesPage
    form_class = ServicesForm
    inline_form_set = ServicesBlockFormset
    template_name = 'pages/services_page_admin.html'
    context_object_name = 'form'


class ContactsPageView(AdminPermissionMixin, UpdateView):
    model = ContactsPage
    form_class = ContactsPageForm
    context_object_name = 'form'
    template_name = 'pages/contacts_page_admin.html'

    def get_object(self, queryset=None):
        return self.model.load()
