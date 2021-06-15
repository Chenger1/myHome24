from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.utils.encoding import escape_uri_path


from db.models.pages import MainPage, AboutPage, ServicesPage, ContactsPage, Document

from website.views.singleton_page_mixin import SingletonView

import mimetypes


class MainPageView(SingletonView):
    model = MainPage
    additional_model = ContactsPage
    template_name = 'pages/main_page.html'


class AboutPageView(SingletonView):
    model = AboutPage
    template_name = 'pages/about.html'


class ServicesPageView(SingletonView):
    model = ServicesPage
    template_name = 'pages/services_page.html'


class ContactsPageView(SingletonView):
    model = ContactsPage
    template_name = 'pages/contacts_page.html'


class DownloadDocument(View):
    model = Document

    def get(self, request, pk):
        """
        We have to user 'escape_uri_path' because of Cyrillic encoding.
        :param request:
        :param pk:
        :return:
        """
        doc = get_object_or_404(self.model, pk=pk)
        path = open(doc.file.path, 'rb')
        response = HttpResponse(path, content_type=mimetypes.guess_type(doc.file.name)[0])
        response['Content-Disposition'] = f'attachment; filename={escape_uri_path(self.file_name(doc.file.name))}'
        return response

    def file_name(self, file):
        return file.split('/')[-1].encode('utf-8')
