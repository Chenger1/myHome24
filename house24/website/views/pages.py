from db.models.pages import MainPage

from website.views.singleton_page_mxin import SingletonView


class MainPageView(SingletonView):
    model = MainPage
    template_name = 'pages/main_page.html'
