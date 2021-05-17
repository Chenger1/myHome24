from django.urls import path

from admin_panel.views.index_views import IndexView


app_name = 'admin_panel'


urlpatterns = [
    path('', IndexView.as_view(), name='index')
]
