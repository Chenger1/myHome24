from db.models.pages import MainPage, AboutPage, ServicesPage

from website.views.singleton_page_mixin import SingletonView


class MainPageView(SingletonView):
    model = MainPage
    template_name = 'pages/main_page.html'


class AboutPageView(SingletonView):
    model = AboutPage
    template_name = 'pages/about.html'


class ServicesPageView(SingletonView):
    model = ServicesPage
    template_name = 'pages/services_page.html'
