from django.urls import path

from user_profile.views import user_views


app_name = 'user_profile'


urlpatterns = [
    path('view/<int:pk>/', user_views.UserProfileView.as_view(), name='user_profile')
]
