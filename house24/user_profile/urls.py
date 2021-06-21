from django.urls import path

from user_profile.views import index


app_name = 'user_profile'


urlpatterns = [
    path('<int:pk>/', index.IndexView.as_view(), name='index')
]