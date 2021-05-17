from django.urls import path

from admin_panel.views.index_views import IndexView
from admin_panel.views.pages.page_views import MainPageView


app_name = 'admin_panel'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    # PAGES
    path('main_page/', MainPageView.as_view(), name='main_page'),
]
