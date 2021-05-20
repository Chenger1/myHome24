from db.models.pages import MainPage, AboutPage, ServicesPage, ContactsPage

from website.views.singleton_page_mixin import SingletonView


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
